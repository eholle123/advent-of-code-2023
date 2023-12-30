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
    is_stepped_plot: Optional[bool] = False

Tiles = NewType("Tiles", Dict[str, List[Tile]])

def read_input(input_file: Path) -> List[List[str]]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [[l for l in line.strip()] for line in lines]

def find_starting_tile(lines: List[List[str]]) -> List[int]:
    for row, line in enumerate(lines):
        for col, l in enumerate(line):
            if l == "S":
                return [row, col]
    return [0, 0]

def parse_tiles(lines: List[List[str]], steps_to_take: int) -> Tiles:
    start_row, start_col = find_starting_tile(lines)
    tiles = {}
    tiles["."] = []
    tiles["O"] = []
    tiles["#"] = []
    tiles_list = lines
    row = 0
    flag = True
    for line in lines:
        col = 0
        for l in line:
            tile = Tile(name=l, row=row, col=col)
            if l == "S":
                tiles["S"] = Tile(name="S", row=start_row, col=start_col)
            else:
                if flag:
                    manhatten = abs(start_row - row) + abs(start_col - col)
                    if (l == ".") and (manhatten <= steps_to_take):
                        tiles_list[row][col] = "O"
                        tile.name = "O"
                        tiles["O"].append(tile)
                    flag = False
                else:
                    flag = True
                if tile.name != "O":
                    tiles[l].append(tile)
            col += 1
        row += 1
    return Tiles(tiles)


def is_stepped_plot(lines: List[List[str]], 
                    tiles: Tiles,
                    possible_plot: Tuple[int, int],
                    steps_to_take: int
                    ) -> Tiles:
    steps = 0
    s_tile = tiles["S"]
    # while steps <= steps_to_take:
    #     if 
    #     steps = steps - 1

    
    return tiles
    

if __name__ == "__main__":
    start_time = time.time()

    steps_to_take = 6
    # steps_to_take = 64
    lines = read_input(Path("inputs/test_input_6_steps_yields_16_plots.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    # ic(lines)

    # ic(find_starting_tile(lines))
    tiles = parse_tiles(lines, steps_to_take)
    # ic(tiles)

    # for possible_plot in tiles:
    #     print(possible_plot)


    
   
    """
    Correct answer for Part 1: 
    """

    print("--- %s seconds ---" % round((time.time() - start_time), 2))

    

