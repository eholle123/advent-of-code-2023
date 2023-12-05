from pathlib import Path
from typing import List, Optional, Dict
from pprint import pprint


valid_game_definition = {'red': 12, 'green': 13, 'blue': 14}

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_game(line: str) -> List[List[Dict[str,int]]]:
    game_number, game_data = line.split(':')
    game_holder, game_num_holder = game_number.split()
    game_num = int(game_num_holder.lstrip())
    game_data.lstrip()
    rounds = parse_round(game_data)
    game = [game_num, rounds]
    return game


def parse_round(game_data: str) -> List[Dict[str,int]]:
    rounds_data = game_data.split(';')
    rounds = []
    for round in rounds_data:
        cubes_revealed_per_round = (round.lstrip()).split(',')
        rounds.append(parse_reveal(cubes_revealed_per_round))
    return rounds


def parse_reveal(cubes_revealed_per_round: List[str]) -> Dict[str,int]:
    cubes = {}
    for cubes_revealed in cubes_revealed_per_round:
        num_cube, cube_color = (cubes_revealed.lstrip()).split()
        num = int(num_cube.lstrip())
        color = cube_color.lstrip()
        cubes[color] = num
    return cubes


def is_game_valid(game: List[Dict[str,int]]) -> bool:
    return all(is_round_valid(round) for round in game) 


def is_round_valid(round: Dict[str,int]) -> bool:
    for value in round:
        if round[value] > valid_game_definition[value]:
            return False
    return True


if __name__ == "__main__":
    lines = read_input(Path("inputs/input.txt"))
    games = [parse_game(line) for line in lines]
    valid_game_numbers = [number for (number, game) in games if is_game_valid(game)]
    print(sum(valid_game_numbers))