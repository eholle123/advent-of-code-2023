from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key

# @dataclass 
# class Node:
#     parent_node: str
#     child_node_L: str
#     child_node_R: str

@dataclass
class Network:
    nodes: Dict[str,Tuple[str,str]]
    start_nodes: List[str]
    end_nodes: List[str]

@dataclass
class Camel_Map:
    network: Dict[str,Tuple[str,str]]
    start_nodes: List[str]
    end_nodes: List[str]
    directions: List[str]

@dataclass
class Path: 
    start_node: str
    end_node: str
    steps_taken: int

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]

def parse_node(line: str) -> List[str]:
    parent_node, node_directions = (line.lstrip()).split("=")
    parent_node = parent_node.replace(' ', '')
    node_directions = ((node_directions.replace('(', ' ')).replace(')', ' ')).replace(' ', '')
    child_node_L, child_node_R = node_directions.split(',')
    return [parent_node, child_node_L, child_node_R]

def parse_network(network_text: List[str]) -> Network:
    network_nodes = {}
    starting_nodes = []
    end_nodes = []
    for node_text in network_text:
        parent_node, child_node_L, child_node_R = parse_node(node_text)
        if parent_node[2] == 'A':
            starting_nodes.append(parent_node)
        if parent_node[2] == 'Z':
            end_nodes.append(parent_node)
        network_nodes[parent_node] = tuple([child_node_L, child_node_R])
    return Network(nodes=network_nodes, start_nodes=starting_nodes, end_nodes=end_nodes)

def get_camel_map(lines) -> Camel_Map:
    network = parse_network(lines[2:-1])
    start_nodes = network.start_nodes
    end_nodes = network.end_nodes
    directions = [direction for direction in lines[0]]
    return Camel_Map(network=network.nodes, start_nodes=start_nodes, end_nodes=end_nodes,directions=directions)

def steps_taken(camel_map: Camel_Map) -> List[List[int]]:
    start_nodes = camel_map.start_nodes
    steps_taken_by_start_nodes= []
    for start_node in start_nodes:
        steps_by_start_node = steps_taken_by_start_node(start_node, camel_map)
        steps_taken_by_start_nodes.append(steps_by_start_node)
        print(steps_taken)
    return steps_taken_by_start_nodes

def steps_taken_by_start_node(start_node: str, camel_map) -> List[int]:
    end_nodes = camel_map.end_nodes
    steps_to_end_nodes = []
    for end_node in end_nodes:
        steps_to_end_node = steps_taken_by_end_node(start_node, end_node, camel_map, 0)
        steps_to_end_nodes.append(steps_to_end_node)
    print(steps_to_end_nodes)
    return steps_to_end_nodes

def steps_taken_by_end_node(start_node: str, end_node: str, camel_map: Camel_Map, steps_taken: int) -> int:
    network = camel_map.network
    next_node = start_node
    for direction in camel_map.directions:
        print(next_node)
        # print(network[next_node])
        # print(direction)
        if next_node == end_node:
            return steps_taken
        else:
            next_node = get_next_node(network[next_node], direction)
            steps_taken += 1
    # print(next_node)
    if next_node != end_node:
        # print("looping through again")
        steps_taken = steps_taken_by_end_node(next_node, end_node, camel_map, steps_taken)
    return steps_taken
        
    

def get_next_node(current_node: Tuple[str,str], direction: str) -> str:
    if direction == 'L':
        next_node = current_node[0]
    else:
        next_node = current_node[1]
    return next_node


if __name__ == "__main__":
    lines = read_input(Path("inputs/test_input_part2_6_steps.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    # directions = [direction for direction in lines[0]]
    # network = parse_network(lines[2:-1])
    camel_map = get_camel_map(lines)
    
    pprint(camel_map)
    print()

    # steps_taken_by_path = steps_taken(camel_map)
    # print(steps_taken_by_path)