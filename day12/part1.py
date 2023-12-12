from __future__ import annotations
import networkx as nx
import itertools
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key


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


if __name__ == "__main__":
    lines = read_input(Path("inputs/test_input_sum_arrangement_counts_21.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    pprint(parse_line(lines[0]))
