# Pawnhub

CLI listing of your online chess games, with special attention brought to the data visualization of the opening sequences.
Discover which lines are your kryptonite and how well you memorize lines of your repertoire.

## Install

pip3 install pawnhub

Note: [pgn-extract](https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/) is required if you intend to use the [repertoire heatmap](https://kraymer.github.io/pawnhub/#repertoire-heatmap) feature.

## Usage

```
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

Use the `--rw` flag to specify a lichess study as your repertoire with white pieces
(`--rb` for black).  
When doing so, games moves are colored to indicate when you deviated from your
repertoire lines.

Here, as white, user played an Italian game when—based on his repertoire—he was supposed to play a Scotch :

 
<div class="term-container"> ♟  1  ⚰️   Hikaru      <span style="color: #4EFF0F;">1. e4 e5 2. Nf3 Nc6 </span><span style="color: #CC0002;">3. Bc4</span><span style="color: #4EFF0F;"> (d4)</span> Nf6 4. Nc3 Bb4</div>


Gold color is used when it is your opponent that brings you into _the unknown_ :

<div class="term-container"> ♟  1  🏳    Danya      <span style="color: #4EFF0F;">1. e4 e5 2. Nf3 Nc6 3. d4</span></span><span style="color: #C4A000;">h6</span> 4. dxe5 g5</div>