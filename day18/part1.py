from __future__ import annotations
import networkx as nx
import time
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
class Dig:
    direction: Optional[str] = ""
    distance: Optional[int] = 0
    color: Optional[str] = ""
    position: Optional[Tuple[int,int]] = None
    is_ground_level: bool = False

@dataclass
class DigPlan:
    digs: List[Dig]
    max_cols: int
    max_rows: int


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_digs(lines: List[str]) -> DigPlan:
    digs = []
    col_num = 0
    row_num = 0
    col_nums = []
    row_nums = []
    for line in lines:
        direction, distance, color = line.split(" ")
        color = (color.replace("(","")).replace(")","")
        dig = Dig(direction=direction.lstrip(), distance=int(distance.lstrip()), color=color.lstrip())
        if (d := dig.distance):
            if dig.direction == "R":
                col_num = col_num + dig.distance
            elif dig.direction == "L":
                col_num = col_num - dig.distance
            elif dig.direction == "U":
                row_num = row_num - dig.distance
            elif dig.direction == "D":
                row_num = row_num + dig.distance
            else:
                ic("Invalid direction.")
            col_nums.append(abs(col_num))
            row_nums.append(abs(row_num))
        digs.insert(0,dig)
    # ic(col_nums)
    # ic(row_nums)
    ic(row_num)
    ic(col_num)
    return DigPlan(digs=digs, max_cols=max(col_nums) + 1, max_rows=max(row_nums) + 1)

def do_dig_plan(dig_plan: DigPlan):
    terrain_hash = [["." for n in range(dig_plan.max_cols + 2)] for m in range(dig_plan.max_rows + 2)]
    terrain = nx.Graph()
    for m in range(dig_plan.max_rows + 2):
        for n in range(dig_plan.max_cols + 2):
            terrain.add_node((m, n), dig=Dig(is_ground_level=True))
    # ic(terrain_hash)
    # ic(len(terrain_hash))
    # ic(len(terrain_hash[0]))
    digs = dig_plan.digs
    # new_digs = []
    # i = dig_plan.max_rows - 2
    # j = dig_plan.max_cols - 2
    i = 1
    j = 1
    hashes = 1
    while len(digs) != 0:
        dig = digs.pop()
        # previous_node = terrain.nodes.get((i, j))
        if (d := dig.distance):
            if dig.direction == "R":
                for jj in range(dig.distance):
                    terrain_hash[i][j + jj] = "#"
                    hashes += 1
                    if node := terrain.nodes.get((i, j + jj)):
                        dig.position = (i, j + jj)
                        node["dig"] = dig
                        terrain.add_edge((i, j + jj), (i, j + jj + 1), color=dig.color)
                        # previous_node = node
                # terrain_hash[i][j:(j + dig.distance)] = ["#" for jj in range(dig.distance)]
                j = j + dig.distance 
            elif dig.direction == "L":
                for jj in range(dig.distance):
                    
                    if node := terrain.nodes.get((i, j - jj)):
                        dig.position = (i, j - jj)
                        node["dig"] = dig
                        terrain.add_edge((i, j - jj), (i, j - (jj + 1)), color=dig.color)
                # terrain_hash[i][(j - dig.distance):j] = ["#" for jj in range(dig.distance)]
                for jc in range(dig.distance+1):
                    terrain_hash[i][j - jc] = "#"
                    hashes += 1
                j = j - dig.distance
            elif dig.direction == "D":
                for ii in range(dig.distance):
                    terrain_hash[i + ii][j] = "#"
                    if node := terrain.nodes.get((i + ii, j)):
                        dig.position = (i + ii, j)
                        node["dig"] = dig
                        terrain.add_edge((i + ii, j), (i + ii + 1, j), color=dig.color)
                # terrain_hash[i:(i + dig.distance)][j] = ["#" for ii in range(dig.distance)]
                i = i + dig.distance
            elif dig.direction == "U":
                for ii in range(dig.distance):
                    # terrain[i-(ii)][j] = "#"
                    
                    if node := terrain.nodes.get((i - ii, j)):
                        dig.position = (i + ii, j)
                        node["dig"] = dig
                        terrain.add_edge((i - ii, j), (i - (ii + 1), j), color=dig.color)
                # terrain_hash[(i - dig.distance):i][j] = ["#" for ii in range(dig.distance)]
                for ir in range(dig.distance+1):
                    terrain_hash[i - ir][j] = "#"
                    hashes += 1
                i = i - dig.distance
            else:
                ic("Not valid direction.")
        # ic(dig)
        # ic(terrain)
        # print()
        # new_digs.append(dig)
        # ic(terrain_hash)
    return [terrain, terrain_hash, hashes]
    # return terrain

if __name__ == "__main__":
    start_time = time.time()

    # lines = read_input(Path("inputs/test_input_yields_62.txt"))
    lines = read_input(Path("inputs/input.txt"))
    # lines = lines[:30]

    dig_plan = parse_digs(lines)
    # ic(dig_plan)
    terrain, terrain_hash, hashes = do_dig_plan(dig_plan)
    # terrain = do_dig_plan(dig_plan)
    # pprint(terrain_hash)
    # ic(terrain_hash)
    ic(hashes)
    nx.drawing.nx_agraph.write_dot(terrain, "terrain.dot")
    cycle = nx.find_cycle(terrain, source=(1, 1))

     # Have to construct both a polygon and points to see if a tile is inside loop.
    polygon = Polygon([vertice[0] for vertice in cycle])
    vertices = [p[0] for p in cycle]
    points = [Point(row, col) 
              for col in range(dig_plan.max_cols) 
              for row in range(dig_plan.max_rows) 
            #   if (row, col) not in vertices 
              ]

    pool = ProcessPool()
    tiles_within_polygon = [
        is_contained
        for is_contained in pool.map(lambda point: polygon.contains(point), points)
        if is_contained
    ]

    ic(len(tiles_within_polygon) + len(vertices))
    
    """
    Correct answer for part 1: 
    Time to run: 
    """
    print("--- %s seconds ---" % round((time.time() - start_time), 2))
    nx.drawing.nx_agraph.write_dot(terrain, "terrain.dot")
