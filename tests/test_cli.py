from pawnhub import numerize_turns


def test_numerize_turns():
    assert numerize_turns(["e4", "e5"]) == ["1.", "e4", "e5"]
