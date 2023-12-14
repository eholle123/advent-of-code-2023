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


# @dataclass
# class Cube:
#     row: int
#     col: int
#     spheres_before: int


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def transpose_lines(lines: List[str] | List[List[str]]) -> List[str]:
    new_lines = []
    for row in range(len(lines[0])):
        new_row = ""
        for col in range(len(lines)):
            new_row += lines[col][row]
        new_lines.append(new_row)
    return new_lines


def roll_rocks_by_col(row: str) -> str:
    if "#" in row:
        cube_rocks = row.count("#")
        row_splices = row.split("#")
        if row_splices[-1] == "":
            el = row_splices.pop()
        rolled_row = ""
        count_cubes = 0
        for row_splice in row_splices:
            rolled_row = rolled_row + get_rolled(row_splice)
            if count_cubes < cube_rocks:
                rolled_row = rolled_row + "#"
                count_cubes += 1
    else:
        rolled_row = get_rolled(row)
    return rolled_row


def get_rolled(row_splice: str) -> str:
    rolled = ""
    round_rocks = len([n for n in row_splice if n != "."])
    rolled = ("0" * round_rocks) + ("." * (len(row_splice) - round_rocks))
    # ic(rolled)
    return rolled


def get_load(rolled_rocks_lines: List[str]) -> int:
    load = 0
    for i, row in enumerate(rolled_rocks_lines):
        count_round = len([r for r in row if ((r != ".") and (r != "#"))])
        load += count_round * (len(rolled_rocks_lines) - i)
    return load


if __name__ == "__main__":
    start_time = time.time()

    # lines = read_input(Path("inputs/test_input_yields_136.txt"))
    lines = read_input(Path("inputs/input.txt"))
    # ic(lines)
    lines_reversed = list(lines.__reversed__())
    # ic(transpose_lines(lines))

    transposed_lines = transpose_lines(lines)
    rolled_rocks_lines = []
    round_rocks = 0
    for row in transposed_lines:
        rolled_row = roll_rocks_by_col(row)
        rolled_rocks_lines.append(rolled_row)
    lengths = [len(row) for row in rolled_rocks_lines]
    # ic(rolled_rocks_lines)
    # ic(lengths)
    # ic('.O...#O..O')
    # ic(roll_rocks_by_col(transposed_lines[2]))
    # ic(transpose_lines((rolled_rocks_lines)))

    rocks_rolled_north = transpose_lines(rolled_rocks_lines)
    load = get_load(rocks_rolled_north)
    ic(load)

    print("--- %s seconds ---" % round((time.time() - start_time), 2))

    """
    Answer Part 1: 105623
    """
