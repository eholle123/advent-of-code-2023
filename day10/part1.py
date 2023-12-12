import networkx as nx
import itertools
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key
from math import lcm


"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, 
    but your sketch doesn't show what shape the pipe has.
"""

# cardinal_directions = ['north', 'south', 'east', 'west']
# NORTH = re.fullmatch(r"north")

pipe_types = {"|": {"north": True, "east": False, "south": True, "west": False},
                "-": {"north": False, "east": True, "south": False, "west": True},
                "L": {"north": True, "east": True, "south": False, "west": False},
                "J": {"north": True, "east": False, "south": False, "west": True},
                "7": {"north": False, "east": False, "south": True, "west": True},
                "F": {"north": False, "east": True, "south": True, "west": False},
                # ".": {"north": False, "east": False, "south": False, "west": False},
                "S": {"north": True, "east": True, "south": True, "west": True}}
"""
"|" can connect to:
    only pipes with same col num:
        if row -1 (pipe above "|") and "south" == True for above pipe:
            connects = ["|", "7", "F"]
        if row +1 (pipe below "|") and "north" == True for below pipe:
            connects = ["|", "L", "J"]
"-" can connect to:
    only pipes with same row num:
        if col -1 (pipe left "-") and "east" == True for left pipe:
            connects = ["-", "L", "F"]
        if col +1 (pipe right "-") and "west" == True for right pipe:
            connects = ["-", "J", "7"] 
"L" can connect to:
    only to pipes directly above or directly right:
        if row -1 (pipe above "L") and "south" == True for above pipe:
            connects = ["|", "7", "F"]
        if col +1 (pipe right "L") and "west" == True for right pipe:
            connects = ["-", "J", "7"]
"J" can connect to:
    only to pipes directly above or directly left:
        if row -1 (pipe above "J") and "south" == True for above pipe:
            connects = ["|", "7", "F"]
        if col -1 (pipe left "J") and "east" == True for left pipe:
            connects = ["-", "L", "F"]
"7" can connect to:
    only to pipes directly left or directly below:
        if col -1 (pipe left "7") and "east" == True for left pipe:
            connects = ["-", "L", "F"]
        if row +1 (pipe below "7") and "north" == True for below pipe:
            connects = ["|", "L", "J"]
"F" can connect to:
    only to pipes directly right or directly below:
        if col +1 (pipe right "L") and "west" == True for right pipe:
            connects = ["-", "J", "7"]
        if row +1 (pipe below "F") and "north" == True for below pipe:
            connects = ["|", "L", "J"]
"S" == pipe such that:
    let "S": {"north": True, "east": True, "south": True, "west": True}
    if pipe above has "south" == False:
        "S"["north"] = False
        "S" in ["-", "7", "F"]
    if pipe below has "north" == False:
        "S"["south"] = False
        "S" in ["-", "L", "J"]
    if pipe right has "west" == False:
        "S"["east"] = False
        "S" in ["-", "7", "J"]
    if pipe left has "east" == False:
        "S"["west"] = False
        "S" in ["-", "L", "F"]
    if all("S".values):
        try every shape?
"""
# tile_types = { pipe_types: 'pipe',
#                 '.': 'ground',
#                 'S': 'starting position'}

# @dataclass
# class WhichCardinals

@dataclass
class Pipe:
    name: str
    shape: Dict[str, bool]
    # north: bool
    # south: bool
    # east: bool
    # west: bool

    # def connects(self, pipe_text: str) -> str:
        

@dataclass
class Tile:
    pipe: Pipe
    row: int
    col: int

    # connects: 
    # steps_from_S: Optional[int]


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_tiles(lines: List[str]) -> List[Tile]:
    tiles = []
    for row, line in enumerate(lines):
        for col, l in enumerate(line):
            if l in pipe_types.keys():
                tile = Tile(pipe=Pipe(name=l, shape=pipe_types[l]), row=row, col=col) 
                tiles.append(tile)
        # pprint(tiles)
    return tiles




def build_graph(tiles: List[Tile]) -> nx.classes.graph.Graph:
    G = nx.Graph()
    for tile in tiles:
        G.add_node(tile)
    # for tile in tiles:
    #     G.add_edge(node.name, network[node.left].name)
    #     G.add_edge(node.name, network[node.right].name)
    return G

if __name__ == "__main__":
    lines = read_input(Path("inputs/finding_loop_tests/test_simple_square_loop_only.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    tiles = parse_tiles(lines)
    pprint(tiles)
