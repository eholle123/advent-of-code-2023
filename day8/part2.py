import networkx as nx
import itertools
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key
from math import lcm


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
    network: Dict[str, Node],
    directions: str,
) -> int:
    steps = 0
    node = network[start_node]
    directions_cycle = itertools.cycle(directions)
    while node.name[-1] != "Z":
        node = network[node.next(next(directions_cycle))]
        steps += 1
    return steps

def build_graph(network: Dict[str, Node]) -> nx.classes.graph.Graph:
    G = nx.Graph()
    for node in network.values():
        G.add_node(node.name)
    for node in network.values():
        G.add_edge(node.name, network[node.left].name)
        G.add_edge(node.name, network[node.right].name)
    return G

if __name__ == "__main__":
    # lines = read_input(Path("inputs/test_input_part2_6_steps.txt"))
    lines = read_input(Path("inputs/input.txt"))
    directions = lines[0]
    network = parse_network(lines[2:])
    start_nodes = [node for node in network.keys() if node[2] == 'A']

    """
    Every 1 unique start node maps to 1 unique end node.
    The path taken from start node -> end node is a unique Loop.
    Each Loop has a specific step count from start node -> end node.
    Must find the least common multiple of step counts from each Loop.
    The lcm is the least number of steps through the network stepping 
    through the network synchronously starting at every start node and 
    stopping when all Loops get to unique end node at the same time.
    """ 
    steps_by_loop = [count_steps(node, network, directions) for node in start_nodes]
    lcm_steps_by_loop = lcm(*steps_by_loop) # *steps_by_loop makes steps_by_loop into a sequence of ints
    print(lcm_steps_by_loop)

    G = build_graph(network)
    print(G)
    nx.drawing.nx_agraph.write_dot(G, "network.dot")
