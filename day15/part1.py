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


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_line(line: str) -> List[str]:
    return line.split(",")


def hashes_to_current_values(strs_to_hash: List[str]) -> List[int]:
    current_values = []
    for str_to_hash in strs_to_hash:
        current_values.append(hash_to_current_value(str_to_hash)) 
    return current_values


def hash_to_current_value(str_to_hash: str) -> int:
    current_value = 0
    for c in str_to_hash:
        current_value += ord(c)
        current_value = current_value * 17
        current_value = current_value % 256
    return current_value


if __name__ == "__main__":
    start_time = time.time()

    # lines = read_input(Path("inputs/test_input_yields_1320.txt"))
    lines = read_input(Path("inputs/input.txt"))
    # ic(lines)
    strs_to_hash = parse_line(lines[0])
    current_values = hashes_to_current_values(strs_to_hash)
    # ic(current_values)
    ic(sum(current_values))
   
    """
    Correct answer for Part 1: 517965
    """

    print("--- %s seconds ---" % round((time.time() - start_time), 2))

    

