from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key



    # | is a vertical pipe connecting north and south.
    # - is a horizontal pipe connecting east and west.
    # L is a 90-degree bend connecting north and east.
    # J is a 90-degree bend connecting north and west.
    # 7 is a 90-degree bend connecting south and west.
    # F is a 90-degree bend connecting south and east.
    # . is ground; there is no pipe in this tile.
    # S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

cardinal_directions = ['north', 'south', 'east', 'west']
pipe_types = {'|': ['north', 'south'],
                '-': ['east', 'west'],
                'L': ['north', 'east'],
                'J': ['north', 'west'],
                '7': ['south', 'west'],
                'F': ['south', 'east'],
                'S': 'starting position'}
# tile_types = { pipe_types: 'pipe',
#                 '.': 'ground',
#                 'S': 'starting position'}

@dataclass
class Tile:
    tile_contents: str
    is_pipe: bool
    # connects: 
    # steps_from_S: Optional[int]


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_tiles_from_line(line: str) -> List[Tile]:
    return [Tile(tile_contents=l, is_pipe=is_pipe(l)) for l in line]

def is_pipe(tile_contents: str) -> bool:
    if tile_contents in pipe_types.keys():
        return True
    else:
        return False

if __name__ == "__main__":
    lines = read_input(Path("inputs/finding_loop_tests/test_simple_square_loop_only.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    sketch_of_pipes = [line for line in lines]
    pprint(parse_tiles_from_line(sketch_of_pipes[1]))
