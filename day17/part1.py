from __future__ import annotations
import networkx as nx
import time
import numpy as np
from shapely import Polygon, Point
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from icecream import ic
from pathos.pools import ProcessPool

"""

"""

# pipe_types = {
#     "|": {"north": True, "east": False, "south": True, "west": False},
#     "-": {"north": False, "east": True, "south": False, "west": True},
#     "L": {"north": True, "east": True, "south": False, "west": False},
#     "J": {"north": True, "east": False, "south": False, "west": True},
#     "7": {"north": False, "east": False, "south": True, "west": True},
#     "F": {"north": False, "east": True, "south": True, "west": False},
#     ".": {"north": False, "east": False, "south": False, "west": False},
# }


# @dataclass
# class Connections:
#     north: bool
#     south: bool
#     east: bool
#     west: bool

#     @staticmethod
#     def parse(s: str) -> Optional[Connections]:
#         if cardinals := pipe_types.get(s):
#             return Connections(**cardinals)

#     def determine_pipe_name(self) -> str:
#         if all(
#             [
#                 self.north == True,
#                 self.south == True,
#                 self.east == False,
#                 self.west == False,
#             ]
#         ):
#             return "|"
#         if all(
#             [
#                 self.north == False,
#                 self.south == False,
#                 self.east == True,
#                 self.west == True,
#             ]
#         ):
#             return "-"
#         if all(
#             [
#                 self.north == True,
#                 self.south == False,
#                 self.east == True,
#                 self.west == False,
#             ]
#         ):
#             return "L"
#         if all(
#             [
#                 self.north == True,
#                 self.south == False,
#                 self.east == False,
#                 self.west == True,
#             ]
#         ):
#             return "J"
#         if all(
#             [
#                 self.north == False,
#                 self.south == True,
#                 self.east == False,
#                 self.west == True,
#             ]
#         ):
#             return "7"
#         if all(
#             [
#                 self.north == False,
#                 self.south == True,
#                 self.east == True,
#                 self.west == False,
#             ]
#         ):
#             return "F"
#         raise ValueError("Cannot determine pipe name for {self}.")


# @dataclass
# class Pipe:
#     name: str
#     connections: Connections


@dataclass
class Block:
    row: int
    col: int 
    heat_loss: int
    visited: bool = False
    distance_from_source: Optional[int] = None
    # path_traveled: Optional[List[Tuple[int,int]]] = None

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_blocks(lines: List[str]) -> List[Block]:
    city_map = []
    for row, line in enumerate(lines):
        for col, l in enumerate(line):
            city_map.append(Block(row=row, col=col, heat_loss=int(l)))
    return city_map

# def parse_blocks(lines: List[str]) -> Dict[Tuple[int,int],int]:
#     city_map = {}
#     for row, line in enumerate(lines):
#         for col, l in enumerate(line):
#             city_map[(row, col)] = int(l)
#     return city_map


def build_graph(lines: List[str], city_map: List[Block]) -> nx.classes.graph.Graph:
    G= nx.Graph()
    H = nx.grid_2d_graph(len(lines), len(lines[0]))
    # G = nx.relabel_nodes(G, city_map)

    for block in city_map:
        G.add_node((block.row, block.col), heat_loss=block.heat_loss)
    
    GcomposeH = nx.compose(G,H)
    
    return GcomposeH


# def determine_start_tile(graph: nx.Graph) -> Tile:
#     start_node, start_tile = [
#         (node, data["tile"])
#         for node, data in graph.nodes.items()
#         if data["tile"].start_tile
#     ][0]

#     connections = Connections(north=False, south=False, east=False, west=False)
#     position_north = (start_node[0] - 1, start_node[1])
#     position_south = (start_node[0] + 1, start_node[1])
#     position_east = (start_node[0], start_node[1] + 1)
#     position_west = (start_node[0], start_node[1] - 1)

#     if north_node_data := graph.nodes.get(position_north):
#         if north_pipe := north_node_data["tile"].pipe:
#             if north_pipe.connections.south:
#                 connections.north = True
#     if south_node_data := graph.nodes.get(position_south):
#         if south_pipe := south_node_data["tile"].pipe:
#             if south_pipe.connections.north:
#                 connections.south = True
#     if east_node_data := graph.nodes.get(position_east):
#         if east_tile := east_node_data["tile"].pipe:
#             if east_tile.connections.west:
#                 connections.east = True
#     if west_node_data := graph.nodes.get(position_west):
#         if west_tile := west_node_data["tile"].pipe:
#             if west_tile.connections.east:
#                 connections.west = True

#     pipe_name = connections.determine_pipe_name()
#     start_pipe = Pipe(name=pipe_name, connections=connections)
#     start_tile = Tile(
#         row=start_node[0], col=start_node[1], pipe=start_pipe, start_tile=True
#     )
#     return start_tile


# def connect_pipes_in_graph(G: nx.Graph, tiles: List[Tile]) -> nx.Graph:
#     for tile in tiles:
#         if tile.is_not_dot:
#             position = (tile.row, tile.col)
#             position_east = (tile.row, tile.col + 1)
#             position_south = (tile.row + 1, tile.col)
#             connections = G.nodes[position]["tile"].pipe.connections
#             if node_data_east := G.nodes.get(position_east):
#                 connections_east = node_data_east["tile"].pipe.connections
#                 if connections.east and connections_east.west:
#                     G.add_edge(position, position_east)
#             if node_data_south := G.nodes.get(position_south):
#                 connections_south = node_data_south["tile"].pipe.connections
#                 if connections.south and connections_south.north:
#                     G.add_edge(position, position_south)
#     return G


if __name__ == "__main__":
    start_time = time.time()

    lines = read_input(Path("inputs/test_input_yields_102.txt"))
    # lines = read_input(Path("inputs/input.txt"))
    # ic(lines)

    blocks = parse_blocks(lines)
    ic(blocks)
    G = build_graph(lines, blocks)

    nx.drawing.nx_agraph.write_dot(G, "blocks.dot")

    """
    Correct answer for part 1: 
    Time to run: 
    """
    print("--- %s seconds ---" % round((time.time() - start_time), 2))
