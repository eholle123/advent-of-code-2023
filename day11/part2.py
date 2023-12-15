from __future__ import annotations
import networkx as nx
import itertools
import re
import numpy as np
import matplotlib.pyplot as plt
import time
from shapely import Polygon, Point, MultiPoint
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key
from math import lcm
from icecream import ic

Position = NewType("Position", Tuple[int, int])  # Tuple(row, col)


@dataclass
class Galaxy:
    position: Position
    number: int


def read_input(input_file: Path) -> List[List[str]]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [[l for l in line.strip()] for line in lines]


def expansion_at_which_rows(lines: List[List[str]]) -> Dict[int, int]:
    # returns a dictionary with keys of which rows are empty and values the number of times the universe has expanded in rows
    which_rows = {}
    expansions = 0
    for row, line in enumerate(lines):
        if "#" not in line:
            expansions += 1
        which_rows[row] = expansions
    return which_rows


def expansion_at_which_cols(lines: List[List[str]]) -> Dict[int, int]:
    # returns a dictionary with keys of which cols are empty and values the number of times the universe has expanded in cols
    lines_transpose = transpose_lines(lines)
    which_cols = {}
    expansions = 0
    for col, line_transpose in enumerate(lines_transpose):
        if "#" not in line_transpose:
            expansions += 1
        which_cols[col] = expansions
    return which_cols


def transpose_lines(lines: List[List[str]]) -> List[List[str]]:
    return [
        [lines[col][row] for col in range(len(lines))] for row in range(len(lines[0]))
    ]


def get_galaxies(
    universe_unexpanded: List[List[str]],
    rows_where_expansion: Dict[int, int],
    cols_where_expansion: Dict[int, int],
    expansion_number: int,
) -> List[Galaxy]:
    galaxies = []
    count_galaxies = 1
    for row, entries in enumerate(universe_unexpanded):
        if "#" in entries:
            for col, entry in enumerate(entries):
                if "#" == entry:
                    row_galaxy = (
                        row
                        + (expansion_number * rows_where_expansion[row])
                        - rows_where_expansion[row]
                    )
                    col_galaxy = (
                        col
                        + (expansion_number * cols_where_expansion[col])
                        - cols_where_expansion[col]
                    )
                    galaxies.append(
                        Galaxy(
                            position=Position((row_galaxy, col_galaxy)),
                            number=count_galaxies,
                        )
                    )
                    count_galaxies += 1
    return galaxies


def steps_between_two_galaxies(position_1: Position, position_2: Position) -> int:
    return abs(position_1[0] - position_2[0]) + abs(position_1[1] - position_2[1])


def find_steps_between_all_galaxy_pairs(
    galaxies: List[Galaxy],
) -> Dict[Tuple[int, int], int]:
    # returns dictionary with galaxy pair numbers as keys and their respective steps from each other as values
    galaxy_pairs = list(itertools.combinations(list(range(1, len(galaxies) + 1)), 2))

    galaxy_pair_distances = {}
    for galaxy_pair in galaxy_pairs:
        galaxy_1_num, galaxy_2_num = galaxy_pair
        position_1 = galaxies[galaxy_1_num - 1].position
        position_2 = galaxies[galaxy_2_num - 1].position
        galaxy_pair_distances[galaxy_pair] = steps_between_two_galaxies(
            position_1, position_2
        )

    return galaxy_pair_distances


if __name__ == "__main__":
    start_time = time.time()

    # universe = read_input(Path("inputs/test_input_yields_36_pairs_and_sum_374.txt"))
    universe = read_input(Path("inputs/input.txt"))
    # ic(universe)

    universe_expansion_at_which_rows = expansion_at_which_rows(universe)
    universe_expansion_at_which_cols = expansion_at_which_cols(universe)
    # ic(universe_expansion_at_which_rows)
    # ic(universe_expansion_at_which_cols)

    galaxies = get_galaxies(
        universe,
        universe_expansion_at_which_rows,
        universe_expansion_at_which_cols,
        1000000,
    )
    # ic(galaxies)

    galaxy_pair_distances = find_steps_between_all_galaxy_pairs(galaxies)
    # ic(galaxy_pair_distances)
    sum_distances = 0
    for distance in galaxy_pair_distances.values():
        sum_distances += distance
    ic(sum_distances)  
    """
    Correct answer for Part 2: 707505470642
    """

    print("--- %s seconds ---" % round((time.time() - start_time), 2))
