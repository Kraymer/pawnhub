from rich.text import Text

RESULT = {
    "W": Text(" 1", style="not dim bold white on dark_green"),
    "L": Text(" 0", style="not dim white on dark_red"),
    "D": Text(" ½", style="not dim on black"),
}
TERMINATION = {
    "abandoned": " 🏳 ",
    "agreed": " ⏸ ",
    "checkmated": " ⚰️ ",
    "insufficient": " ⏹ ",
    "stalemate": " ⏹ ",
    "repetition": " 🔁 ",
    "resigned": " 🏳 ",
    "timeout": " 🕰 ",
}

WHITE_CONSOLE_INSTR = "grey62 on white"
BLACK_CONSOLE_INSTR = "grey62 on black"
COLOR = {
    "chess.com": {
        True: Text(" ♟", style=f"not dim {WHITE_CONSOLE_INSTR}"),
        False: Text(" ♟", style=f"not dim {BLACK_CONSOLE_INSTR}"),
    },
    "lichess.org": {
        True: Text(" ♞", style=f"not dim {WHITE_CONSOLE_INSTR}"),
        False: Text(" ♞", style=f"not dim {BLACK_CONSOLE_INSTR}"),
    },
    None: {
        True: Text(" ●", style=f"not dim {WHITE_CONSOLE_INSTR}"),
        False: Text(" ●", style=f"not dim {BLACK_CONSOLE_INSTR}"),
    },
}


def as_link(text, url):
    return f"[link={url}]{text}[/link]"


def as_int(text):
    if text:
        return "{}".format(int(text))
    return ""
