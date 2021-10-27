===============================================
SC21 `Students@SC` Boardgame Tournament Scoring
===============================================

This repository contains the Python code that is used to determine the winners of the `Students@SC` Boardgame Tournament.

Dependencies
============

The Python code in this repository depends on the following:

- Python 3
- `Pandas <https://pandas.pydata.org/>`_
- `Numpy <https://numpy.org/>`_
- `Tomli <https://github.com/hukkin/tomli>`_

Usage
=====

The main driver for this code is the :code:`boardgame_tournament_ranker.ipynb` Jupyter Notebook. All the code used in the notebook can be found in the :code:`boardgame_tournament_scoring` directory.

To use the notebook, a Configuration file and a Score file are required. The specifications for these files can be found below. Then, to get results, simply run the cells of the Jupyter Notebook.

Configuration File Specification
--------------------------------

The configuration file is a TOML file that provides relevant data on each game in the tournament. At the top of the file, there must be a :code:`config_id` field. This is simply used as a unique ID for the file. Each game in the file must have the following format:

.. code-block:: toml
   [game_name]
   max_ranking_points = ...
   number_of_scores = ...
   number_of_players = ...
   placement_based = [True|False]

The fields for each game are as follows:

- :code:`game_name`: the name (i.e., unique identifier) of the game
- :code:`max_ranking_points`: the maximum number of points that this game can contribute towards a contestant's overall score
- :code:`number_of_scores`: the number of scores that this game will contribute towards a contestant's overall score
- :code:`number_of_players`: the maximum number of players for the game
- :code:`placement_based`: if true, scores for this game should be interpreted as placements (i.e., rankings in a single instance of the game).

Check out :code:`test.toml` for an example of a configuration file.

Score File Specification
------------------------

The score file is a CSV file containing information about the results of games played. Each row in this file represents a single contestant's result for a single instance of a game. There are three columns in this file:

1) The :code:`name` column, which specifies the contestant's name
2) The :code:`game` column, which specifies the game the contestant played
3) The :code:`score` column, which specifies the contestant's score/placement in the game

The only other requirement for the score file is that entries in the :code:`game` column **must** match one of the :code:`game_name` fields in the configuration file. If an entry does not match one of these fields, the row will be treated as if it represents an unknown game, and, thus, it will be dropped.

Check out :code:`test.csv` for an example of a score file.
