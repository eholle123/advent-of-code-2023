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
    is_start: Optional[bool] = False

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

def parse_tiles(lines: List[List[str]], steps_to_take: int) -> List[Tile] | List[List[str]]:
    start_row, start_col = find_starting_tile(lines)
    max_dim = steps_to_take + steps_to_take - 1
    # unneeded_edges = len(lines) - max_dim
    unneeded_edges = 0
    if unneeded_edges == 0:
        lower_bound = 0
        upper_bound = len(lines)
    else:
        lower_bound = int(unneeded_edges/2)
        upper_bound = -int(unneeded_edges/2)
    # marked_lines = lines[lower_bound:upper_bound]
    # marked_lines = [marked_line[lower_bound:upper_bound] for marked_line in marked_lines]
    tiles = []
    tiles_list = lines
    row = 0
    flag = True
    for line in lines:
        col = 0
        for l in line:
            tile = Tile(name=l, row=row, col=col)
            if tile.name == "S":
                # start_position = [row, col]
                tile.is_start = True
            if flag:
                manhatten = abs(start_row - row) + abs(start_col - col)
                if (l == ".") and (manhatten <= steps_to_take):
                    tiles_list[row][col] = "O"
                    tile.name = "O"
                flag = False
            else:
                flag = True
            tiles.append(tile)
            col += 1
        row += 1
    # ic(tiles_list)
    return tiles_list
    
def mark_possible_plots(lines: List[str], steps_to_take: int) -> List[str]:
    start_row, start_col = find_starting_tile(lines)
    
    # ic(marked_lines)
    # ic(len(marked_lines))
    # ic(len(marked_lines[0]))
    # start_row, start_col = find_starting_tile(marked_lines)
    # ic(start_row, start_col)
    # row = 0
    # col = 0
    # for marked_line in marked_lines:
    #     for tile in marked_line:
    #         if (row % 2 == 0) and (tile == "."): 
    #             # marked_lines[row][col] = "O"
    #         col += 1
    #     row += 1
    # return marked_lines
    pass

    

if __name__ == "__main__":
    start_time = time.time()

    # steps_to_take = 64
    steps_to_take = 6
    lines = read_input(Path("inputs/test_input_6_steps_yields_16_plots.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    ic(lines)
    ic(len(lines[0]))
    ic(len(lines))
    # ic(64+64+1)
    # ic(lines[0][2])
    # lines[0][2] = lines[0][2].replace(".", "O")
    # ic(lines[0][2])
    ic(find_starting_tile(lines))
    # marked_lines = mark_possible_plots(lines, steps_to_take)
    tiles = parse_tiles(lines, steps_to_take)
    start_row, start_col = find_starting_tile(tiles)
    # ic(tiles)
    
   
    """
    Correct answer for Part 1: 
    """

    print("--- %s seconds ---" % round((time.time() - start_time), 2))

    

