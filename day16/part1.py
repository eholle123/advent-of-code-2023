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

# UNKNOWNS = re.compile(r"(\?+)")

"""
- If the beam encounters empty space (.), it continues in the same direction.
- If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror.
    - a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column.
    - a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
- If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. 
    - a rightward-moving beam that encounters a - splitter would continue in the same direction.
- If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, 
    - a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
"""

tile_types = {
    "|": {"north": True, "east": False, "south": True, "west": False},
    "-": {"north": False, "east": True, "south": False, "west": True},
    "/": {"north": True, "east": False, "south": False, "west": True},
    "\\": {"north": False, "east": True, "south": True, "west": False}, # \ is \\ because can't use "\"
    ".": {"north": True, "east": True, "south": True, "west": True},
}


@dataclass
class Connections:
    north: bool
    south: bool
    east: bool
    west: bool

    @staticmethod
    def parse(s: str) -> Optional[Connections]:
        if cardinals := tile_types.get(s):
            return Connections(**cardinals)

    def determine_pipe_name(self) -> str:
        if all(
            [
                self.north == True,
                self.south == True,
                self.east == False,
                self.west == False,
            ]
        ):
            return "|"
        if all(
            [
                self.north == False,
                self.south == False,
                self.east == True,
                self.west == True,
            ]
        ):
            return "-"
        if all(
            [
                self.north == False,
                self.south == True,
                self.east == True,
                self.west == False,
            ]
        ):
            return "L"
        if all(
            [
                self.north == True,
                self.south == False,
                self.east == False,
                self.west == True,
            ]
        ):
            return "/"
        if all(
            [
                self.north == True,
                self.south == True,
                self.east == True,
                self.west == True,
            ]
        ):
            return "."
        raise ValueError("Cannot determine pipe name for {self}.")


@dataclass
class Mirror:
    name: str
    connections: Connections


@dataclass
class Splitter:
    name: str
    connections: Connections

    def parse(self, s: str):
        if s == "/":
            self.name = "/"
            self.connections.parse("/")
        else:
            self.name = "\\"
            self.connections.parse("\\")


@dataclass
class Tile:
    row: int
    col: int  # things that don't have a default have to go above things that do
    splitter: Optional[Splitter]
    mirror: Optional[Mirror]
    is_energized: bool = True
    is_not_dot: bool = True

@dataclass
class LightBeam:
    direction: Connections


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


# def parse_line(line: str) -> Spring:
#     conditions, nums_text = (line.lstrip()).split(" ")
#     nums = [int(num) for num in nums_text.split(",")]
#     return Spring(conditions=conditions, contiguous_group_of_damaged_springs=nums)


if __name__ == "__main__":
    lines = read_input(Path("inputs/test_input_46_tiles_energized.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    ic(lines)
