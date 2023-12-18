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

UNKNOWNS = re.compile(r"(\?+)")

@dataclass
class Spring:
    conditions: str
    contiguous_group_of_damaged_springs: List[int]

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_line(line: str) -> Spring:
    conditions, nums_text = (line.lstrip()).split(" ")
    nums = [int(num) for num in nums_text.split(",")]
    return Spring(conditions=conditions, contiguous_group_of_damaged_springs=nums)


def get_spring_condition_permutations(spring: Spring) -> int:
    conditions_subs = (spring.conditions).split
    res = UNKNOWNS.finditer(springs[3].conditions)
    unknowns_groups = [r.group() for r in res]
    if len(unknowns_groups) == 1:
        

    pass


if __name__ == "__main__":
    lines = read_input(Path("inputs/test_input_sum_arrangement_counts_21.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    ic(lines)
    springs = [parse_line(line) for line in lines]
    ic(springs)
    ic(UNKNOWNS.match(springs[0].conditions))
    ic(UNKNOWNS.match(".??..??...?##."))

    
    # ic([''.join(c) for c in itertools.permutations(springs[0].conditions)])
