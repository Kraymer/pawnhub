# Pawnhub

CLI listing of your online chess games, with special attention brought to the data visualization of the opening sequences.
Discover which lines are your kryptonite and how well you memorize lines of your repertoire.

## Install

pip3 install pawnhub

Note: [pgn-extract](https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/) is required if you intend to use the [repertoire heatmap](https://kraymer.github.io/pawnhub/#repertoire-heatmap) feature.

## Usage

~~~
Usage: pawnhub.py [OPTIONS]

  List games for CHESSCOM_USER and LICHESS_USER.

  Display for each game the first move out of repertoire if WHITE_REP or/and
  BLACK_REP are given.

Options:
  -c, --chesscom_user CHESSCOM_USER
                                  chess.com user login
  -l, --lichess_user LICHESS_USER
                                  lichees.org user login
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
~~~ 

### Repertoire heatmap
<style>.term-container {
  background: #171717;
  border-radius: 5px;
  color: white;
  word-break: break-word;
  overflow-wrap: break-word;
  font-family: Monaco, courier;
  font-size: 12px;
  line-height: 20px;
  padding: 14px 18px;
  white-space: pre-wrap;
}
</style>

<div style="background: #171717;"> ♟  1  ⚰️   madhavkuikel      88 5+5  Kings Fianchetto Opening           <span style="color: #ffffaf;">1. g3 d5 2. b4 e5 3. Bg2</span> Nf6 4. e3 Bd7 5. Nf3 e4 6. Ne5 Bxb4 7. c3 Bd6 8. d4 Nc6</div>
