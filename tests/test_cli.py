from dataclasses import dataclass
import pawnhub


@dataclass
class Game:
    white: bool


def test_numerize_turns():
    assert pawnhub.numerize_turns(["e4", "e5"]) == ["1.", "e4", "e5"]


def test_sanitize_prefix():
    assert pawnhub.sanitize_prefix(["1.", "e4", "e5", "2."]) == ["1.", "e4", "e5"]


def test_status_first_move_out_line():
    game = Game(white=False)
    assert (
        pawnhub.status_first_move_out_line(game, ["1.", "d4", "Nf6", "2.", "Bf4", "c5"])
        == pawnhub.MoveStatus.OUT_OF_REP
    )
