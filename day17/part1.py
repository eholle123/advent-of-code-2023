from __future__ import annotations
import networkx as nx
import time
import numpy as np
from shapely import Polygon, Point
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from icecream import ic
from pathos.pools import ProcessPool

"""

"""


@dataclass
class Block:
    row: int
    col: int 
    heat_loss: int
    visited: bool = False
    distance_from_source: Optional[int] = None
    # path_traveled: Optional[List[Tuple[int,int]]] = None

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_blocks(lines: List[str]): # returns a np.array
    city_map = np.zeros((len(lines), len(lines[0])), dtype=int)
    for i, line in enumerate(lines):
        for j, l in enumerate(line):
            city_map[i, j] = int(l)
    return city_map

# def parse_blocks(lines: List[str]) -> Dict[Tuple[int,int],int]:
#     city_map = {}
#     for row, line in enumerate(lines):
#         for col, l in enumerate(line):
#             city_map[(row, col)] = int(l)
#     return city_map

# def parse_blocks(lines: List[str]) -> List[Block]:
#     city_map = []
#     for row, line in enumerate(lines):
#         for col, l in enumerate(line):
#             city_map.append(Block(row=row, col=col, heat_loss=int(l)))
#     return city_map

def build_graph(lines: List[str], city_map: List[Block]) -> nx.classes.graph.Graph:
    G= nx.Graph()
    H = nx.grid_2d_graph(len(lines), len(lines[0]))
    # G = nx.relabel_nodes(G, city_map)
    for block in city_map:
        G.add_node((block.row, block.col), heat_loss=block.heat_loss)
    GcomposeH = nx.compose(G,H)
    return GcomposeH

def dijkstras_algorithm(blocks, source: Tuple[int, int], goal: Tuple[int, int]) -> int:
    max_row = len(blocks)
    max_col = len(blocks[0])
    # ic(max_row)
    # ic(max_col)
    d  = blocks * np.inf
    d[0, 0] = 0 # distances from source matrix
    # ic(d)
    visited = np.array(blocks, bool) * False
    # ic(visited)
    paths = {}
    paths[source] = (0,0)
    ic(paths)
    to_goal = False
    x_current, y_current = source
    # ic(x_current, y_current)
    # ic(blocks[x_current, y_current])
    # while not to_goal:
    #     if x_current < max_row - 1: # block below
    #         if ((d[x_current, y_current] + blocks[x_current + 1, y_current]) < d[x_current + 1, y_current]) and (visited[x_current + 1, y_current] is False):
    #             d[x_current + 1, y_current] = d[x_current, y_current] + blocks[x_current + 1, y_current]
    #             paths[x_current + 1, y_current] = (x_current, y_current)

    #     if y_current < max_col -1: # block to the right
    #         if ((d[x_current, y_current] + blocks[x_current, y_current + 1]) < d[x_current, y_current + 1]) and (visited[x_current, y_current + 1] is False):
    #             d[x_current, y_current + 1] = d[x_current, y_current] + blocks[x_current, y_current + 1]
    #             paths[x_current, y_current + 1] = (x_current, y_current)
        
    #     if x_current > 0: # block above
    #         if ((d[x_current, y_current] + blocks[x_current - 1, y_current]) < d[x_current - 1, y_current]) and (visited[x_current - 1, y_current] is False):
    #             d[x_current - 1, y_current] = d[x_current, y_current] + blocks[x_current - 1, y_current]
    #             paths[x_current - 1, y_current] = (x_current, y_current)
        
    #     if y_current > 0: # block to the left
    #         if ((d[x_current, y_current] + blocks[x_current, y_current - 1]) < d[x_current, y_current - 1]) and (visited[x_current, y_current - 1] is False):
    #             d[x_current, y_current - 1] = d[x_current, y_current] + blocks[x_current, y_current - 1]
    #             paths[x_current, y_current - 1] = (x_current, y_current)

    #     if x_current > 0:
    #         x
    #     if x_current == max_row and y_current == max_col:
    #         to_goal = True
        
    return 0


if __name__ == "__main__":
    start_time = time.time()

    lines = read_input(Path("inputs/test_input_yields_102.txt"))
    # lines = read_input(Path("inputs/input.txt"))

    ic(lines)

    blocks = parse_blocks(lines)
    ic(blocks)
    # G = build_graph(lines, blocks)

    lcp = dijkstras_algorithm(blocks, (0,0), (len(lines), len(lines[0]))) # lcp = lowest_cost_path
    ic(lcp)

    # nx.drawing.nx_agraph.write_dot(G, "blocks.dot")

    """
    Correct answer for part 1: 
    Time to run: 
    """
    print("--- %s seconds ---" % round((time.time() - start_time), 2))
