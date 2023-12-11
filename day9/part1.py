from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_sequence(line: str) -> List[int]:
    sequence_strs = line.split(" ")
    sequence = [int(s) for s in sequence_strs]
    return sequence


def make_sequence_tree(sequence: List[int]) -> List[List[int]]:
    sequence_tree = [sequence]
    while (all([num == 0 for num in sequence]) is False) and len(sequence) > 1:
        sub_sequence = get_sub_sequence(sequence)
        sequence_tree.append(sub_sequence)
        sequence = sub_sequence
    sequence_tree = sequence_tree[-1::-1]
    return sequence_tree


def get_sub_sequence(sequence: List[int]) -> List[int]:
    return [
        (sequence[i + 1] - sequence[i])
        for i, num in enumerate(sequence)
        if i + 1 != len(sequence)
    ]


def predict_next_value_in_sequence(
    sequence_tree: List[List[int]], last_value: int
) -> List[List[int]]:
    next_value = 0
    for sequence in sequence_tree:
        next_value = last_value + sequence[-1]
        sequence.append(next_value)
        last_value = sequence[-1]
    return sequence_tree


def get_predicted_values(oasis_and_sand_sensor_data: List[List[int]]) -> List[int]:
    predicted_values = []
    for sequence in oasis_and_sand_sensor_data:
        sequence_tree = make_sequence_tree(sequence)
        sequence_tree = predict_next_value_in_sequence(sequence_tree, 0)
        next_value = sequence_tree[-1][-1]
        predicted_values.append(next_value)
    return predicted_values


if __name__ == "__main__":
    # lines = read_input(Path("inputs/test_input_yields_114.txt"))
    lines = read_input(Path("inputs/input.txt"))
    oasis_and_sand_sensor_data = [parse_sequence(line) for line in lines]
    # pprint(oasis_and_sand_sensor_data)

    predicted_values = get_predicted_values(oasis_and_sand_sensor_data)
    print(sum(predicted_values))
