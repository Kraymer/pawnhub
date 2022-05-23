import logging
import os
import click
import re
import tempfile
import shutil
import subprocess
import random

from enum import Enum

import chess.pgn
import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text
from pawnstore import pawnstore
from pawnstore.models import Game
from pawnstore.services import parse_game

import display

APP_TEMP_DIR = os.path.join(tempfile.gettempdir(), "pawnhub")

logger = logging.getLogger(__name__)
console = Console()
table = Table(
    collapse_padding=True,
    expand=True,
    row_styles=["dim", ""],
    padding=(0,),
    show_header=False,
    show_edge=False,
    show_lines=False,
    box=None,
)


class MoveStatus(Enum):
    FORGET = 1
    OUT_OF_REP = 2


def numerize_turns(lst):
    """Add turn indicators.
    ["e4", "e5"] => ["1.", "e4", "e5"]
    """
    res = []
    for idx, item in enumerate(lst):
        if idx % 2 == 0:
            res.append(f"{idx/2+1:.0f}.")
        res.append(item)
    return res


def sanitize_prefix(prefix):
    """Remove last item if it is a turn indicator
    "1. e4 e5 2." => "1. e4 e5"
    """
    if prefix[-1].endswith("."):
        prefix.pop()
    return prefix


def status_first_move_out_line(game, moves_rep_in):
    """Return status of first move outside preparation"""
    if game.white and len(moves_rep_in) % 3 == 0:
        status = MoveStatus.FORGET
    elif not game.white and len(moves_rep_in) % 3 == 2:
        status = MoveStatus.FORGET
    else:
        status = MoveStatus.OUT_OF_REP
    return status


def categorize_from_repertoire(moves, line):
    """Return a tuple of two strings representing moves in repertoire followed
    by moves outside it.
    """
    prefix = sanitize_prefix(os.path.commonprefix([moves, line]))

    idx = len(prefix)
    if idx == len(line):
        good_move_idx = idx
    else:
        good_move_idx = idx + line[idx].endswith(".")
    return (moves[:idx], moves[idx:], line[good_move_idx : good_move_idx + 1])


def display_game_moves(game, line):
    moves = numerize_turns(game.moves.split(" "))

    moves = moves[:24]

    if line:
        line = numerize_turns(line.split(" "))

        moves_rep_in, moves_rep_out, good_move = categorize_from_repertoire(moves, line)
        moves_str = Text("")
        moves_str.append(" ".join(moves_rep_in), style="bold green")
        if not moves_rep_out:
            return moves_str
        idx = 0
        status_first_move_out = status_first_move_out_line(game, moves_rep_in)
        if moves_str:
            moves_str.append(" ")
        while True:
            moves_str.append(
                moves_rep_out[idx] + " ",
                style=f'{"red" if status_first_move_out == MoveStatus.FORGET else "yellow"} not dim',
            )
            if not moves_rep_out[idx].endswith("."):
                break
            idx += 1
        if status_first_move_out == MoveStatus.FORGET and good_move:
            good_move = Text(f"({good_move[0]}) ")
            good_move.stylize("green", 1, -2)
            moves_str.append(good_move)
        moves_str.append(" ".join(moves_rep_out[idx + 1 :]))

    else:
        moves_str = Text(" ".join(moves))

    return moves_str


def find_repertoire_line(game, repertoire):
    res = None
    if repertoire[game.white]:
        res = ""

    for line in sorted(repertoire[game.white]):
        if line > game.moves:
            # Pick the "correct" line amongst the two last
            if os.path.commonprefix([game.moves, res]) in os.path.commonprefix(
                [game.moves, line]
            ):
                res = line
            break
        res = line

    return res


def display_game(game, repertoire):

    line = find_repertoire_line(game, repertoire)
    timestamp = game.timestamp
    table.add_row(
        display.COLOR[game.website][game.white],
        display.RESULT[game.result],
        display.TERMINATION.get(game.termination, ""),
        display.as_link(game.opp_name[:17], game.slug),
        display.as_int(game.accuracy),
        game.time_control,
        display.as_link(game.eco_name[:44], repertoire[game.white].get(line, "?")),
        display_game_moves(game, line),
    )


def find(game, search):
    """Search for string in game data.

    search can be free text (whole game search) or formatted as
    field:search to search in a specific field.
    """
    tokens = search.split(":")
    field = None
    if len(tokens) == 2:
        field = tokens[0]
    elif len(tokens) > 2:
        raise Exception("Invalid search")

    text = tokens[-1].lower()

    data = ""
    if field:
        data = str(getattr(game, field))
    else:
        for k, v in game.__data__.items():
            data += str(v)

    if text in data.lower():
        return True


def display_games(store, search, repertoire):
    table.add_column("Side/site")
    table.add_column("Result")
    table.add_column("Termination")
    table.add_column("Opponent")
    table.add_column("Accuracy")
    table.add_column("Time control")
    table.add_column("Opening", style="yellow")
    table.add_column("Moves", no_wrap=False)
    for game in list(store):
        if not search or find(game, search):
            display_game(game, repertoire)
    console.print(table)


def pgn_split_variants(pgn_path):
    out_path = tempfile.NamedTemporaryFile(prefix="pawnhub_").name
    cmd = f"pgn-extract --quiet --splitvariants {pgn_path}"

    with open(out_path, "w") as outfile:
        subprocess.run(cmd, stdout=outfile, shell=True)
    return out_path


def pgn_extract_lines(pgn_path):
    lines = {}
    if pgn_path:
        with open(pgn_path) as pgn:
            while True:
                game = chess.pgn.read_game(pgn)
                if not game:
                    break
                hdr, moves = parse_game(game)
                lines[" ".join(moves)] = game.headers["Site"]
    return {k: lines[k] for k in sorted(lines)}


def build_repertoire(white_pgn_file, black_pgn_file):
    repertoire = {True: {}, False: {}}
    if white_pgn_file:
        repertoire[True] = pgn_extract_lines(pgn_split_variants(white_pgn_file))
    if black_pgn_file:
        repertoire[False] = pgn_extract_lines(pgn_split_variants(black_pgn_file))
    return repertoire


def rewrite_search(ctx, param, value):
    """Convert to non numerized moves sequence"""
    if value:
        return re.sub(r"\d+\.\s", "", value)


class PathOrUrlType(click.ParamType):
    name = "path or url"

    def convert(self, value, param, ctx):
        if os.path.exists(value):
            return value
        else:
            resp = requests.get(f"{value}", stream=True)

            if resp.status_code != 200:
                self.fail(f"{value!r} is not a valid path or url", param, ctx)
            # https://stackoverflow.com/questions/34252553/downloading-file-in-python-with-requests

            with open(os.path.join(APP_TEMP_DIR, param.name + ".pgn"), "wb") as target:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, target)
                return target.name


PATH_OR_URL = PathOrUrlType()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]), help="yadda")
@click.option("-c", "--chesscom_user", default=None)
@click.option("-l", "--lichess_user", default=None)
@click.option(
    "-s",
    "--search",
    default=None,
    metavar="FIELD:TEXT",
    callback=rewrite_search,
    help="Search for text in given field (one of: {}). Omit field to search in whole games data.".format(
        ", ".join(Game.searchable_fields)
    ),
)
@click.option(
    "--rw",
    "white_pgn_file",
    type=PATH_OR_URL,
    # type=click.Path(exists=True),
    metavar="WHITE_FILE",
    nargs=1,
    help="Path or url to a PGN file for white repertoire",
)
@click.option(
    "--rb",
    "black_pgn_file",
    type=PATH_OR_URL,
    metavar="BLACK_FILE",
    nargs=1,
    help="Path or url to a PGN file for black repertoire",
)
def cli(
    chesscom_user=None,
    lichess_user=None,
    search=None,
    white_pgn_file=None,
    black_pgn_file=None,
):
    if not (chesscom_user or lichess_user):
        click.echo(ctx.get_help() + "\n")
        logger.error("Please provide a username")
        exit(1)

    store = pawnstore(chesscom_user, lichess_user)
    repertoire = build_repertoire(white_pgn_file, black_pgn_file)

    display_games(store, search, repertoire)


if __name__ == "__main__":
    if not os.path.exists(APP_TEMP_DIR):
        os.mkdir(APP_TEMP_DIR)
    cli()
