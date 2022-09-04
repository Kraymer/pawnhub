[![nopypi](http://github.com/kraymer/pawnhub/workflows/build/badge.svg)](https://github.com/Kraymer/pawnhub/actions/workflows/python-build.yml)
[![](https://readthedocs.org/projects/pawnhub/badge/?version=latest)](http://pawnhub.readthedocs.org/en/latest/?badge=latest)
[![nopypi](https://codecov.io/gh/Kraymer/pawnhub/branch/main/graph/badge.svg?token=EPMJ5EZGIK)](https://codecov.io/gh/Kraymer/pawnhub)
[![nopypi](http://img.shields.io/pypi/v/pawnhub.svg)](https://pypi.python.org/pypi/pawnhub)
[![](https://pepy.tech/badge/pawnhub)](https://pepy.tech/project/pawnhub)
[![nopypi](https://img.shields.io/badge/releases-atom-orange.svg)](https://github.com/Kraymer/pawnhub/releases.atom)

# pawnhub


Retrieve results of your online chess games from lichess.org and
chess.com.

Instantly see how you negotiated first moves to reach your favourite
positions. Spot which lines are your kryptonite leading to a
dry/deceiving middle game.

Behind the scenes, it exploits
[pawnstore](https://github.com/Kraymer/pawnstore) library to fetch games
into a local database then make them
[rich](https://github.com/Textualize/rich).

**Read documentation at https://pawnhub.readthedocs.io/**

## Screencast

[![asciicast](https://asciinema.org/a/518641.svg)](https://asciinema.org/a/518641)

## Install

`pawnhub` is written for Python 3.7+, install with pip via ``pip3 install pawnhub`` command.

## Usage

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
