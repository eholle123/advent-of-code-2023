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
    game_numbers: Game_Numbers
    game_card: int


@dataclass
class Score_Card:
    game_cards: List[int]
    scores_of_games: List[int]
    counts_of_cards_by_game: List[int]


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_game(line: str) -> Game:
    game_card_number_text, game_data_text = line.split(":")
    return Game(
        game_card=parse_game_card_number(game_card_number_text),
        game_numbers=parse_game_numbers(game_data_text),
    )


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
        if ((number_text.strip()) == "") is False:
            number = int(number_text.strip())
            numbers.append(number)
    return numbers


def count_winning_numbers_in_game(game: Game) -> int:
    game_numbers = game.game_numbers
    count_of_winning_numbers = 0
    for my_number in game_numbers.my_numbers:
        if my_number in game_numbers.winning_numbers:
            count_of_winning_numbers += 1
    return count_of_winning_numbers


def make_score_card(games: List[Game]) -> Score_Card:
    scores_of_games = []
    counts_of_cards_by_game = []
    game_cards = []
    for game in games:
        scores_of_games.append(count_winning_numbers_in_game(game))
        counts_of_cards_by_game.append(1)
        game_cards.append(game.game_card)
    return Score_Card(
        game_cards=game_cards,
        scores_of_games=scores_of_games,
        counts_of_cards_by_game=counts_of_cards_by_game,
    )


def update_score_card(score_card: Score_Card) -> Score_Card:
    for i, current_game_card in enumerate(score_card.game_cards):
        # pprint(score_card)
        score_card.counts_of_cards_by_game = update_counts_of_cards(
            score_card, current_game_card
        )
    return score_card


def add_elementwise(a: List[int], b: List[int]) -> List[int]:
    assert len(a) == len(b), "Lists must have the same length to be added."
    return [element_a + element_b for (element_a, element_b) in zip(a, b)]


def update_counts_of_cards(score_card: Score_Card, current_game_card: int) -> List[int]:
    score = score_card.scores_of_games[(current_game_card - 1)]
    count = score_card.counts_of_cards_by_game[(current_game_card - 1)]
    copies = [0] * len(score_card.game_cards)
    copies[(current_game_card) : (current_game_card) + score] = [1] * len(
        range(0, score)
    )
    for counter in range(count):
        score = score_card.scores_of_games[(current_game_card - 1)]
        while score > 0:
            score_card.counts_of_cards_by_game[current_game_card + score - 1] += 1
            score = score - 1
    return score_card.counts_of_cards_by_game


if __name__ == "__main__":
    lines = read_input(Path("inputs/input.txt"))
    games = [parse_game(line) for line in lines]
    score_card = update_score_card(make_score_card(games))
    pprint(score_card)
    sum_count_of_cards = sum(score_card.counts_of_cards_by_game)
    pprint(sum_count_of_cards)
