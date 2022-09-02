"""
CLI listing your online chess games results
"""

import click_log
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

from pawnhub import display

__version__ = "0.1.0"


APP_TEMP_DIR = os.path.join(tempfile.gettempdir(), "pawnhub")
ERR_PGN_EXTRACT_INSTALL = """pgn-extract is required by the openings heatmap feature (--rw and --rb flags). 
Please download binary from https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/
"""
ERR_LICHESS_API_KEY = """Lichess api key is required, you can create one at https://lichess.org/account/oauth/token
Then declare it via the shell command
    export LICHESS_API_TOKEN=your_key
"""
ERR_MISSING_USERNAME = """Please provide a username.
Try 'pawnhub --help' for more information.
"""

if not os.path.exists(APP_TEMP_DIR):
    os.mkdir(APP_TEMP_DIR)
logger = logging.getLogger(__name__)
click_log.basic_config(logger)

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
    """Return game as serie of moves in short algebric notation.

    Moves present in the repertoire are green.
    First move outside of repertoire is either yellow if the opponent played
    or red if it's the user. In the latter case, the correct move
    (repertoire-wise) is indicated as a variation.
    """
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
    """Return the longest line in the repertoire that has been played in
    game"""
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
    """Add game infos in the table to display"""
    line = find_repertoire_line(game, repertoire)
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


def find(game, searches):
    """Search for string in game data.

    search can be free text (whole game search) or formatted as
    field:search to search in a specific field.
    """
    res = True
    for search in searches:
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
        res &= text in data.lower()
    return res


def display_games(store, search, repertoire, color, lines):
    """Build and display table of games"""
    table.add_column("Side/site")
    table.add_column("Result")
    table.add_column("Termination")
    table.add_column("Opponent")
    table.add_column("Accuracy")
    table.add_column("Time control")
    table.add_column("Opening", style="yellow")
    table.add_column("Moves", no_wrap=False)
    for game in list(store)[-lines:]:
        if not search or find(game, search):
            display_game(game, repertoire)

    console = Console(force_terminal=color)
    console.print(table)


def pgn_split_variants(pgn_path):
    """Split single pgn file into multiples pgn variants files."""
    out_path = tempfile.NamedTemporaryFile(prefix="pawnhub_").name
    cmd = f"pgn-extract --quiet --splitvariants {pgn_path}"

    with open(out_path, "w") as outfile:
        res = subprocess.run(cmd, stdout=outfile, stderr=subprocess.DEVNULL, shell=True)
        if res.returncode == 127:
            logger.error(ERR_PGN_EXTRACT_INSTALL)
            exit(1)
    return out_path


def pgn_extract_lines(pgn_path):
    """Return dict mapping lines to lichess studies

    {'e4 Nf6 e5 Nd5 d4 d6 Nf3': 'https://lichess.org/study/xxxxx', ...}
    """
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
    """Return a dict with two main keys : white lines are accessible under the
    True key, black lines under the False key.
    """
    repertoire = {True: {}, False: {}}
    if white_pgn_file:
        repertoire[True] = pgn_extract_lines(pgn_split_variants(white_pgn_file))
    if black_pgn_file:
        repertoire[False] = pgn_extract_lines(pgn_split_variants(black_pgn_file))
    return repertoire


def rewrite_search(ctx, param, values):
    """Convert values to non numerized moves sequence so that typing
         --search "1. e4 c5 2. Nf3"
    is equivalent to
         --search "e4 c5 Nf3"
    """
    res = []
    for value in values:
        res.append(re.sub(r"\d+\.\s", "", value))
    return res


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


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="""List games for CHESSCOM_USER and LICHESS_USER.\n
Display for each game the first move out of repertoire if WHITE_REP or/and BLACK_REP are given.""",
)
@click.option(
    "-c",
    "--chesscom_user",
    metavar="CHESSCOM_USER",
    default=None,
    help="chess.com user login",
)
@click.option(
    "-l",
    "--lichess_user",
    metavar="LICHESS_USER",
    default=None,
    help="lichees.org user login",
)
@click.option(
    "-n", "--lines", metavar="NUM", default=0, help="Print the NUM most recent games"
)
@click.option(
    "-s",
    "--search",
    default=None,
    metavar="[FIELD:]TEXT",
    callback=rewrite_search,
    multiple=True,
    help="Search for text in given field (see https://kraymer.github.io/pawnhub/#search). Omit FIELD: to search in whole games data.",
)
@click.option(
    "--rw",
    "white_pgn_file",
    type=PATH_OR_URL,
    # type=click.Path(exists=True),
    metavar="WHITE_REP",
    nargs=1,
    help="Path or url to a PGN file for white repertoire",
)
@click.option(
    "--rb",
    "black_pgn_file",
    type=PATH_OR_URL,
    metavar="BLACK_REP",
    nargs=1,
    help="Path or url to a PGN file for black repertoire",
)
@click.option(
    "--color", default=None, is_flag=True, help="Always color terminal output"
)
@click.version_option(__version__)
@click.pass_context
def pawnhub_cli(
    ctx,
    chesscom_user=None,
    lichess_user=None,
    search=None,
    color=False,
    white_pgn_file=None,
    black_pgn_file=None,
    lines=None,
):
    if not (chesscom_user or lichess_user):
        logger.error(ERR_MISSING_USERNAME)
        exit(1)
    if lichess_user and "LICHESS_API_TOKEN" not in os.environ:
        logger.error(ERR_LICHESS_API_KEY)
        exit(1)
    store = pawnstore(chesscom_user, lichess_user)
    repertoire = build_repertoire(white_pgn_file, black_pgn_file)

    display_games(store, search, repertoire, color, lines)
