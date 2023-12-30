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

"""
# = rocks
. = plot
S = start
O = garden plots occupied by step "x"
64 = desired number of steps to take
"""

@dataclass
class Tile:
    name: str
    row: int
    col: int
    # is_start: Optional[bool] = False
    is_stepped_plot: Optional[bool] = False

Tiles = NewType("Tiles", Dict[str, List[Tile]])

def read_input(input_file: Path) -> List[List[str]]:
    with input_file.open("r") as f:
        lines = f.readlines()
    # lines = [[l for l in line.strip()] for line in lines]
    return [[l for l in line.strip()] for line in lines]

def find_starting_tile(lines: List[List[str]]) -> List[int]:
    for row, line in enumerate(lines):
        for col, l in enumerate(line):
            if l == "S":
                return [row, col]
    return [0, 0]

def parse_tiles(lines: List[List[str]], steps_to_take: int) -> List[Tile] | List[List[str]] | Dict[str, Dict[Tuple[int, int], bool]]:
    start_row, start_col = find_starting_tile(lines)
    tiles = []
    tile_plots = {}
    possible_plots = {}
    tiles_list = lines
    row = 0
    flag = True
    for line in lines:
        col = 0
        for l in line:
            tile = Tile(name=l, row=row, col=col)
            if tile.name == "S":
                tile_plots["S"] = (row, col)
            if flag:
                manhatten = abs(start_row - row) + abs(start_col - col)
                if (l == ".") and (manhatten <= steps_to_take):
                    tiles_list[row][col] = "O"
                    tile.name = "O"
                    possible_plots[(row, col)] = False
                flag = False
            else:
                flag = True
            tiles.append(tile)
            col += 1
        row += 1
    # ic(tiles_list)
    return possible_plots


def is_stepped_plot(lines: List[List[str]], 
                    possible_plots: Dict[str, Dict[Tuple[int, int], bool]],
                    possible_plot: Tuple[int, int],
                    steps_to_take: int
                    ) -> Dict[Tuple[int, int], bool]:
    
    

if __name__ == "__main__":
    start_time = time.time()

    steps_to_take = 6
    # steps_to_take = 64
    lines = read_input(Path("inputs/test_input_6_steps_yields_16_plots.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    ic(lines)

    ic(find_starting_tile(lines))
    tiles = parse_tiles(lines, steps_to_take)
    ic(tiles)

    for possible_plot in tiles:
        print(possible_plot)


    
   
    """
    Correct answer for Part 1: 
    """

    print("--- %s seconds ---" % round((time.time() - start_time), 2))

    

