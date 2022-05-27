.. image:: http://img.shields.io/pypi/v/pawnstore.svg
   :target: https://pypi.python.org/pypi/pawnstore
.. image:: https://pepy.tech/badge/pawnstore
   :target: https://pepy.tech/project/pawnstore

.. pypi

pawnhub
=======

Retrieve results of your online chess games from lichess.org and chess.com.    

Instantly see how you negotiated first moves to reach your favourite positions.
Spot which lines are your kryptonite leading to a dry/deceiving middle game.

Behind the scenes, it exploits `pawnstore <https://github.com/Kraymer/pawnstore>`_ library to fetch games into a local database then make them `rich <https://github.com/Textualize/rich>`_.

**Read documentation at https://pawnhub.readthedocs.io/**

Screenshot
----------

.. image:: https://github.com/Kraymer/pawnhub/raw/docs/docs/_static/screenshot.png

Usage
-----

::

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
