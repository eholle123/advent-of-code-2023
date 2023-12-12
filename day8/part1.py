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
class Node:
    name: str
    left: str
    right: str

    def next(self, direction: str) -> str:
        if direction == "L":
            return self.left
        elif direction == "R":
            return self.right
        else:
            raise ValueError(f"Invalid direction '{direction}'. Must be 'L' or 'R'.")


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_node(line: str) -> Node:
    name, children = (line.lstrip()).split("=")
    name = name.replace(" ", "")
    children = ((children.replace("(", " ")).replace(")", " ")).replace(" ", "")
    left, right = children.split(",")
    return Node(name=name, left=left, right=right)


def parse_network(network_text: List[str]) -> Dict[str, Node]:
    network = {}
    for node_text in network_text:
        node = parse_node(node_text)
        network[node.name] = node
    return network


def count_steps(
    start_node: str,
    end_node: str,
    network: Dict[str, Node],
    directions: str,
) -> int:
    steps = 0
    node = network[start_node]
    directions_cycle = itertools.cycle(directions)
    while node.name != end_node:
        node = network[node.next(next(directions_cycle))]
        steps += 1
    return steps


if __name__ == "__main__":
    # lines = read_input(Path("inputs/test_input_equals_2_steps.txt"))
    # lines = read_input(Path("inputs/test_input_equals_6_steps.txt"))
    lines = read_input(Path("inputs/input.txt"))
    directions = lines[0]
    network = parse_network(lines[2:])

    # pprint(directions)
    # print()
    # pprint(network)

    steps_taken = count_steps("AAA", "ZZZ", network, directions)
    print(steps_taken)
