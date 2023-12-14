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


def expand_by_row(lines: List[List[str]]) -> List[List[str]]:
    universe_expanded_by_row = lines[0:]
    row = 0
    for i, line in enumerate(lines):
        if "#" not in line:
            universe_expanded_by_row.insert(row, line)
            row += 1
        row += 1
    return universe_expanded_by_row


def expand_by_col(lines: List[List[str]]) -> List[List[str]]:
    lines_transpose = transpose_lines(lines)
    universe_expanded_by_col = lines_transpose[0:]
    col = 0
    for j, line_transpose in enumerate(lines_transpose):
        if "#" not in line_transpose:
            universe_expanded_by_col.insert(col, line_transpose)
            col += 1
        col += 1
    universe_expanded = transpose_lines(universe_expanded_by_col)
    return universe_expanded


def transpose_lines(lines: List[List[str]]) -> List[List[str]]:
    return [
        [lines[col][row] for col in range(len(lines))] for row in range(len(lines[0]))
    ]


def get_galaxies(universe_expanded: List[List[str]]) -> List[Galaxy]:
    galaxies = []
    count = 1
    for row, entries in enumerate(universe_expanded):
        if "#" in entries:
            for col, entry in enumerate(entries):
                if "#" == entry:
                    galaxies.append(Galaxy(position=Position((row, col)), number=count))
                    count += 1
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

    # lines = read_input(Path("inputs/test_input_yields_36_pairs_and_sum_374.txt"))
    lines = read_input(Path("inputs/input.txt"))
    # ic(lines)

    universe_expanded_by_row = expand_by_row(lines)
    universe_expanded = expand_by_col(universe_expanded_by_row)
    # ic(universe_expanded_by_row)
    # ic(universe_expanded)

    galaxies = get_galaxies(universe_expanded)
    # ic(galaxies)

    galaxy_pair_distances = find_steps_between_all_galaxy_pairs(galaxies)
    sum_distances = 0
    for distance in galaxy_pair_distances.values():
        sum_distances += distance
    ic(sum_distances)

    print("--- %s seconds ---" % round((time.time() - start_time), 2))
