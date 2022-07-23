from dataclasses import dataclass
import pawnhub


@dataclass
class Game:
    white: bool = False
    moves: list = "d4 Nf6 Bf4 c5 e3 cxd4"


repertoire = {
    False: {
        "d4 Nf6 Bf4 c5 d5 b5": "http://example1.com",
        "d4 Nf6 Bf4 c5 e3 b5": "http://example2.com",
    }
}


def test_numerize_turns():
    assert pawnhub.numerize_turns(["e4", "e5"]) == ["1.", "e4", "e5"]


def test_sanitize_prefix():
    assert pawnhub.sanitize_prefix(["1.", "e4", "e5", "2."]) == ["1.", "e4", "e5"]


def test_status_first_move_out_line():
    game = Game()
    assert (
        pawnhub.status_first_move_out_line(game, ["1.", "d4", "Nf6", "2.", "Bf4", "c5"])
        == pawnhub.MoveStatus.OUT_OF_REP
    )


def test_find_repertoire_line():
    assert pawnhub.find_repertoire_line(Game(), repertoire) == "d4 Nf6 Bf4 c5 e3 b5"
