from __future__ import annotations
import networkx as nx
import itertools
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key
from math import lcm
from icecream import ic

"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, 
    but your sketch doesn't show what shape the pipe has.
"""

pipe_types = {"|": {"north": True, "east": False, "south": True, "west": False},
                "-": {"north": False, "east": True, "south": False, "west": True},
                "L": {"north": True, "east": True, "south": False, "west": False},
                "J": {"north": True, "east": False, "south": False, "west": True},
                "7": {"north": False, "east": False, "south": True, "west": True},
                "F": {"north": False, "east": True, "south": True, "west": False}}

@dataclass
class Connections:
    north: bool
    south: bool
    east: bool
    west: bool

    @staticmethod
    def parse(s: str) -> Optional[Connections]:
        if (cardinals := pipe_types.get(s)):
            return Connections(**cardinals)
        
    def determine_pipe_name(self) -> str:
        if all([self.north == True, self.south == True, self.east == False, self.west == False]):
            return "|"
        if all([self.north == False, self.south == False, self.east == True, self.west == True]):
            return "-"
        if all([self.north == True, self.south == False, self.east == True, self.west == False]):
            return "L"
        if all([self.north == True, self.south == False, self.east == False, self.west == True]):
            return "J"
        if all([self.north == False, self.south == True, self.east == False, self.west == True]):
            return "7"
        if all([self.north == False, self.south == True, self.east == True, self.west == False]):
            return "F"
        raise ValueError("Cannot determine pipe name for {self}.")



@dataclass
class Pipe:
    name: str
    connections: Connections
      

@dataclass
class Tile:
    row: int
    col: int #things that don't have a default have to go above things that do
    pipe: Optional[Pipe] = None 
    start_tile: bool = False

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_tiles(lines: List[str]) -> List[Tile]:
    tiles = []
    for row, line in enumerate(lines):
        for col, l in enumerate(line):
            if (connections := Connections.parse(l)):
                tile = Tile(pipe=Pipe(name=l, connections=connections), row=row, col=col) 
                tiles.append(tile)
            if l == "S":
                tile = Tile(row=row, col=col, start_tile=True)
                tiles.append(tile)
    return tiles

def build_graph(tiles: List[Tile]) -> nx.classes.graph.Graph:
    G = nx.Graph()
    for tile in tiles:
        G.add_node((tile.row, tile.col), tile=tile)
    return G

def determine_start_tile(graph: nx.Graph) -> Tile:
    start_node, start_tile = [
        (node, data["tile"])
        for node, data in graph.nodes.items()
        if data["tile"].start_tile
    ][0]

    connections = Connections(north=False, south=False, east=False, west=False)
    position_north = (start_node[0] - 1, start_node[1])
    position_south = (start_node[0] + 1, start_node[1])
    position_east = (start_node[0], start_node[1] + 1)
    position_west = (start_node[0], start_node[1] - 1)

    if (north_node_data := graph.nodes.get(position_north)):
        if (north_pipe := north_node_data["tile"].pipe):
            if north_pipe.connections.south:
                connections.north = True
    if (south_node_data := graph.nodes.get(position_south)):
        if (south_pipe := south_node_data["tile"].pipe):
            if south_pipe.connections.north:
                connections.south = True
    if (east_node_data := graph.nodes.get(position_east)):
        if (east_tile := east_node_data["tile"].pipe):
            if east_tile.connections.west:
                connections.east = True
    if (west_node_data := graph.nodes.get(position_west)):
        if (west_tile := west_node_data["tile"].pipe):
            if west_tile.connections.east:
                connections.west = True
    
    pipe_name = connections.determine_pipe_name()
    start_pipe = Pipe(name=pipe_name, connections=connections)
    start_tile = Tile(row=start_node[0], col=start_node[1], pipe=start_pipe, start_tile=True)
    return start_tile

def valid_connection_east(pipe_connections: Connections, pipe_east_connections: Connections) -> bool:
    return (pipe_connections.east and pipe_east_connections.west)

def valid_connection_south(pipe_connections: Connections, pipe_south_connections: Connections) -> bool:
    return (pipe_connections.south and pipe_south_connections.north)

def connect_pipes_in_graph(G: nx.Graph, tiles: List[Tile]) -> nx.Graph:
    for tile in tiles:
        position = (tile.row, tile.col)
        position_east = (tile.row, tile.col + 1)
        position_south = (tile.row + 1, tile.col)
        connections = G.nodes[position]["tile"].pipe.connections
        if (node_data_east := G.nodes.get(position_east)):
            connections_east = node_data_east["tile"].pipe.connections
            if (connections.east and connections_east.west):
                G.add_edge(position, position_east)
        if (node_data_south := G.nodes.get(position_south)):
            connections_south = node_data_south["tile"].pipe.connections
            if (connections.south and connections_south.north):
                G.add_edge(position, position_south)
    return G


if __name__ == "__main__":
    # lines = read_input(Path("inputs/part1/test_simple_square_loop_only.txt"))
    # lines = read_input(Path("inputs/part1/test_simple_square_loop.txt"))
    # lines = read_input(Path("inputs/part1/test_complex_loop.txt"))
    lines = read_input(Path("inputs/input.txt"))
    tiles = parse_tiles(lines)

    G = build_graph(tiles)
    
    start_tile = determine_start_tile(G)
    G.add_node((start_tile.row, start_tile.col), tile=start_tile)
    connect_pipes_in_graph(G, tiles)
    cycle = nx.find_cycle(G, source=(start_tile.row, start_tile.col))
    # ic(cycle)
    # pprint(str(G))
    max_distance = len(cycle) // 2
    print(max_distance)


    nx.drawing.nx_agraph.write_dot(G, "tiles.dot")
    

