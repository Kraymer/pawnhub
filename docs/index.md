# Pawnhub

> _“Which do I prefer? Sex or chess? It depends on the position.”_ -- Boris Spassky

> **PH** *noun.* 1. popular website with people mating in different positions 2. terminal chess database client to review your own games and update your repertoire accordingly

## Features

- One centralized database : your go-to terminal command to have an overview of your chess games results whether online or OTB
- [Searching](https://pawnhub.readthedocs.io/en/latest/index.html#searching) : easy yet powerful filtering capabilities to focus your analysis on subset of games (lost, white pieces, sicilians, etc)
- [Openings heatmap](https://pawnhub.readthedocs.io/en/latest/index.html#openings-heatmap) : possible to specify your repertoire via lichess etudes and visualize which lines gives best/worse results based on your games data

## Install

`pip3 install pawnhub`


## Getting started

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
  -s, --search [FIELD:]TEXT       Search for text in given field (cf
                                  [Searching](https://pawnhub.readthedocs.io/en/latest/#searching).
                                  Omit FIELD: to search in whole games data.
  --rw WHITE_REP                  Path or url to a PGN file for white repertoire
  --rb BLACK_REP                  Path or url to a PGN file for black repertoire
  --color                         Always color terminal output
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.
```

## Advanced usage

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

### Openings heatmap

```{note}
[pgn-extract](https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/) tool is required to use this feature.
```

If you have your repertoire lines stored in lichess studies[^lichess-study] then your games moves can be colored to indicate when you deviated from your
theoretical lines.
Use the `--rw` flag to specify a lichess study as your repertoire with white pieces
(`--rb` for black).  

Here, as white, user played an Italian game when—based on his repertoire—he was supposed to play a Scotch :

<div class="term-container"> ♟ <span style="background-color: #005F00;"> 1 </span> ⚰️   Hikaru      <span style="color: #005F00;">1. e4 e5 2. Nf3 Nc6 </span><span style="color: #CC0002;">3. Bc4</span><span style="color: #005F00;"> (d4)</span> Nf6 4. Nc3 Bb4 ...</div>


Gold color is used when it is your opponent that brings you into _the unknown_ :

<div class="term-container"> ♟ <span style="background-color: #005F00;"> 1 </span> 🏳    Danya      <span style="color: #005F00;">1. e4 e5 2. Nf3 Nc6 3. d4</span></span> <span style="color: #C4A000;">h6</span> 4. dxe5 g5 ...</div>


So the longest green streak the better.  
Hitting a gold move early is a sign that you should add data to your repertoire etude to stay in the theory.  
Whereas red means you haven't memorized your repertoire lines.


[^lichess-study]: cf https://lichess.org/study/search?q=repertoire for examples of studies used as repertoires
