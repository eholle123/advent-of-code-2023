from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key


# @dataclass
# class Hand:
#     cards: str
#     bid: int
#     hand_type: str

#     @property
#     def hand_type_sort_value(self) -> int:
#         return hand_types[self.hand_type]

#     @property
#     def sort_key(self) -> Tuple[int, List[int]]:
#         return (self.hand_type_sort_value, [camel_cards[card] for card in self.cards])


@dataclass
class Node:
    parent_node: str
    child_node_L: str
    child_node_R: str


# Node = NewType("Node", Dict['str', Tuple[str, str]])


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


# def parse_node(line: str) -> Node:
#     parent_node, node_directions = (line.lstrip()).split("=")
#     parent_node = parent_node.replace(' ', '')
#     node_directions = ((node_directions.replace('(', ' ')).replace(')', ' ')).replace(' ', '')
#     child_node_L, child_node_R = node_directions.split(',')
#     return Node(parent_node=parent_node, child_node_L=child_node_L, child_node_R=child_node_R)


def parse_node(line: str) -> List[str]:
    parent_node, node_directions = (line.lstrip()).split("=")
    parent_node = parent_node.replace(" ", "")
    node_directions = ((node_directions.replace("(", " ")).replace(")", " ")).replace(
        " ", ""
    )
    child_node_L, child_node_R = node_directions.split(",")
    return [parent_node, child_node_L, child_node_R]


def parse_network(network_text: List[str]) -> Dict[str, Tuple[str, str]]:
    network = {}
    for node_text in network_text:
        parent_node, child_node_L, child_node_R = parse_node(node_text)
        network[parent_node] = tuple([child_node_L, child_node_R])
    return network


def get_how_many_steps_taken(
    start_node: str,
    end_node: str,
    network: Dict[str, Tuple[str, str]],
    directions: List[str],
    steps_taken: int,
) -> int:
    direction = directions[0]
    next_node = start_node
    for direction in directions:
        # print(next_node)
        # print(network[next_node])
        # print(direction)
        if next_node == end_node:
            return steps_taken
        else:
            next_node = get_next_node(network[next_node], direction, network)
            steps_taken += 1
    # print(next_node)
    if next_node != end_node:
        # print("looping through again")
        steps_taken = get_how_many_steps_taken(
            next_node, end_node, network, directions, steps_taken
        )
    return steps_taken


def get_next_node(
    current_node: Tuple[str, str], direction: str, network: Dict[str, Tuple[str, str]]
) -> str:
    if direction == "L":
        next_node = current_node[0]
    else:
        next_node = current_node[1]
    return next_node


if __name__ == "__main__":
    # lines = read_input(Path("inputs/test_input_equals_2_steps.txt"))
    # lines = read_input(Path("inputs/test_input_equals_6_steps.txt"))
    lines = read_input(Path("inputs/input.txt"))
    directions = [direction for direction in lines[0]]
    network = parse_network(lines[2:-1])

    # pprint(directions)
    # print()
    # pprint(network)

    steps_taken = get_how_many_steps_taken("AAA", "ZZZ", network, directions, 0)
    print(steps_taken)
