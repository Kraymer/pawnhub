# Pawnhub

> _“Which do I prefer? Sex or chess? It depends on the position.”_ -- Boris Spassky

Retrieve results of your online chess games from lichess.org and chess.com.  
Instantly see how you negotiated first moves to reach your favourite positions.
Spot which lines are your kryptonite that lead to a dry/deceiving middle game.

Pawnhub helps you keep your repertoire up-to-date based on real data in order to 
improve your mastery of <s>foreplay</s> openings.

## Install

`pip3 install pawnhub`


## Usage

```text
Usage: pawnhub.py [OPTIONS]

  List games for CHESSCOM_USER and LICHESS_USER.

  Display for each game the first move out of repertoire if WHITE_REP or/and
  BLACK_REP are given.

Options:
  -c, --chesscom_user CHESSCOM_USER
                                  chess.com user login
  -l, --lichess_user LICHESS_USER
                                  lichess.org user login
  -n, --lines NUM                 Print the NUM most recent games
  -s, --search [FIELD:]TEXT       Search for text in given field (see
                                  https://kraymer.github.io/pawnhub/#search).
                                  Omit FIELD: to search in whole games data.
  --rw WHITE_REP                  Path or url to a PGN file for white
                                  repertoire
  --rb BLACK_REP                  Path or url to a PGN file for black
                                  repertoire
  --color                         Always color terminal output
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.
```

### Openings heatmap

```{note}
Note: [pgn-extract](https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/) is required to use the this feature.
```

Use the `--rw` flag to specify a lichess study as your repertoire with white pieces
(`--rb` for black).  
When doing so, games moves are colored to indicate when you deviated from your
repertoire lines.

Here, as white, user played an Italian game when—based on his repertoire—he was supposed to play a Scotch :

 
<div class="term-container"> ♟ <span style="background-color: #005F00;"> 1 </span> ⚰️   Hikaru      <span style="color: #005F00;">1. e4 e5 2. Nf3 Nc6 </span><span style="color: #CC0002;">3. Bc4</span><span style="color: #005F00;"> (d4)</span> Nf6 4. Nc3 Bb4 ...</div>


Gold color is used when it is your opponent that brings you into _the unknown_ :

<div class="term-container"> ♟ <span style="background-color: #005F00;"> 1 </span> 🏳    Danya      <span style="color: #005F00;">1. e4 e5 2. Nf3 Nc6 3. d4</span></span> <span style="color: #C4A000;">h6</span> 4. dxe5 g5 ...</div>

### Searching

Use the `-s` option to select games to display based on a specific query.
Indicate on which field to search, followed by the value to match (eg `-s eco:A00`).  
In most cases, skipping the field to search on whole game data is shorter and produce same results (eg `-s A00`).

Below the existing fields and enumeration of their possible values :

| Field       | value                                              |
| ---         | ---                                                |
| eco         | ECO code from `A00` to `E99`                       |
| eco_name    | eg _Benko Gambit_                                  |
| moves       | eg _e4 d5 exd5_ ...                                |
| opp_name    | Opponent name                                      |
| result      | `W` (win), `L` (loss), `D` (draw)                  |
| termination | `timeout`, `resigned`, `checkmated`, `abandoned`   |
| website     | `chess.com`, `lichess.org`                         |
| white       | `0` (no), `1` (yes)                                |
