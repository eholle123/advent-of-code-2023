from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint


@dataclass
class Game_Numbers:
    winning_numbers: List[int]
    my_numbers: List[int]

@dataclass
class Game: 
    game_card: int
    game_numbers: Game_Numbers

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_game(line: str) -> Game:
    game_card_number_text, game_data_text = line.split(":")
    return Game(game_card=parse_game_card_number(game_card_number_text), game_numbers=parse_game_numbers(game_data_text))
    

def parse_game_card_number(game_card_number_text: str) -> int:
    game_holder, game_num_holder = game_card_number_text.split()
    return int(game_num_holder.lstrip())

def parse_game_numbers(game_data_text: str) -> Game_Numbers:
    winning_numbers_text, my_numbers_text = (game_data_text.lstrip()).split("|")
    winning_nums = parse_numbers(winning_numbers_text)
    my_nums = parse_numbers(my_numbers_text)
    return Game_Numbers(winning_numbers=winning_nums, my_numbers=my_nums)

def parse_numbers(numbers_text: str) -> List[int]:
    numbers = []
    for number_text in (numbers_text.lstrip()).split(" "):
        if ((number_text.strip()) == "")  is False:
            number = int(number_text.strip())
            numbers.append(number)
    return numbers

def score_game(game: Game) -> int:
    game_numbers = game.game_numbers
    count_of_winning_numbers = 0
    for my_number in game_numbers.my_numbers:
        if my_number in game_numbers.winning_numbers:
            count_of_winning_numbers += 1 
    if count_of_winning_numbers == 0:
        return 0
    else:
        return 2**(count_of_winning_numbers-1)

if __name__ == "__main__":
    lines = read_input(Path("inputs/input.txt"))
    games = [parse_game(line) for line in lines]
    game_scores = [score_game(game) for game in games]
    # pprint(games)
    # pprint(game_scores)
    pprint(sum(game_scores))
