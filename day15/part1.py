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


if __name__ == "__main__":
    start_time = time.time()

    # lines = read_input(Path("inputs/test_input.txt"))
    lines = read_input(Path("inputs/input.txt"))
    ic(lines)
   
    """
    Correct answer for Part 1: 
    """

    print("--- %s seconds ---" % round((time.time() - start_time), 2))

    

