from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint

Round = NewType("Round", Dict[str, int])


@dataclass
class Game:
    number: int
    rounds: List[Round]


valid_game_definition = {"red": 12, "green": 13, "blue": 14}


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_game(line: str) -> Game:
    game_number, game_data = line.split(":")
    game_holder, game_num_holder = game_number.split()
    game_num = int(game_num_holder.lstrip())
    game_data = game_data.lstrip()
    rounds_data = game_data.split(";")
    rounds = []
    for round_text in rounds_data:
        rounds.append(parse_round(round_text))
    return Game(number=game_num, rounds=rounds)


def parse_round(round_text: str) -> Round:
    counts_by_color = {}
    for pair in (round_text.lstrip()).split(","):
        color, count = parse_pair(pair)
        counts_by_color[color] = count
    return Round(counts_by_color)


def parse_pair(pair: str) -> Tuple[str, int]:
    num_cube, cube_color = (pair.lstrip()).split()
    num = int(num_cube.lstrip())
    color = cube_color.lstrip()
    return (color, num)


def is_game_valid(game: Game) -> bool:
    return all(is_round_valid(round) for round in game.rounds)


def is_round_valid(round: Round) -> bool:
    for value in round:
        if round[value] > valid_game_definition[value]:
            return False
    return True


if __name__ == "__main__":
    lines = read_input(Path("inputs/input.txt"))
    games = [parse_game(line) for line in lines]
    valid_game_numbers = [game.number for game in games if is_game_valid(game)]
    print(sum(valid_game_numbers))
