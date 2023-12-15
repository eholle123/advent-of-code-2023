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


@dataclass
class Lens:
    label: str
    focal_length: int

Boxes = NewType("Boxes", Dict[int, List[Lens]])

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_line(line: str) -> List[str]:
    return line.split(",")

def get_box_number(str_to_hash: str) -> int:
    current_value = 0
    for c in str_to_hash:
        current_value += ord(c)
        current_value = current_value * 17
        current_value = current_value % 256
    return current_value

def get_boxes(lens_configuration_strs: List[str]) -> Boxes:
    boxes = {}
    for lens_text in lens_configuration_strs:
        if "=" in lens_text:
            lens_label, lens_focal_length = lens_text.split("=")
            box_number = get_box_number(lens_label)
            if (lenses := boxes.get(box_number)):
                if any([lens.label == lens_label for lens in lenses]):
                    for index, lens in enumerate(lenses):
                        if lens.label == lens_label:
                            lenses[index].focal_length = int(lens_focal_length)
                            boxes[box_number] = lenses
                            break
                else:
                    lenses.append(Lens(label=lens_label, focal_length=int(lens_focal_length)))
            else:
                boxes[box_number] = [Lens(label=lens_label, focal_length=int(lens_focal_length))]
        else:
            lens_label = lens_text[:-1]
            box_number = get_box_number(lens_label)
            if (lenses := boxes.get(box_number)):
                if any([lens.label == lens_label for lens in lenses]):
                    if len(lenses) == 1:
                        del boxes[box_number]
                    else:
                        for index, lens in enumerate(lenses):
                            if lens.label == lens_label:
                                discard = lenses.pop(index)
                                boxes[box_number] = lenses
                                break
    return Boxes(boxes)


def calculate_focusing_power_of_box(box_number: int, lenses: List[Lens]) -> int:
    box_focusing_power = 0
    for i, lens in enumerate(lenses):
        box_focusing_power += (box_number + 1) * (i + 1) * (lens.focal_length)
    return box_focusing_power

def calculate_focusing_power(boxes: Boxes) -> int:
    focusing_power = 0
    for box in boxes.keys():
        focusing_power += calculate_focusing_power_of_box(box, boxes[box])
    return focusing_power


if __name__ == "__main__":
    start_time = time.time()

    # lines = read_input(Path("inputs/test_input_yields_1320.txt"))
    lines = read_input(Path("inputs/input.txt"))
    # ic(len(lines))

    lens_configuration_strs = parse_line(lines[0])
    # ic(lens_configuration_strs)

    boxes = get_boxes(lens_configuration_strs)
    # ic(boxes)

    focusing_power = calculate_focusing_power(boxes)
    ic(focusing_power)
   
    """
    Correct answer for Part 2: 267372
    """

    print("--- %s seconds ---" % round((time.time() - start_time), 2))