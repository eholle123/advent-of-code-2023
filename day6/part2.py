from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_line(line: str) -> List[int]:
    text, numbers_text = (line.lstrip()).split(":")
    number = int(numbers_text.replace(" ", ""))
    return [number]


def calculate_possible_distances(record_time: int) -> List[int]:
    possible_times = [t for t in range(record_time + 1)]
    possible_speeds = [s for s in range(record_time, -1, -1)]
    possible_distances = [
        time * speed for time, speed in zip(possible_times, possible_speeds)
    ]
    return possible_distances


def ways_to_win(possible_distances: List[int], record_distance: int) -> int:
    distances = []
    if len(possible_distances) % 2 == 0:
        distances = [
            possible_distances[i] for i in range(0, int(len(possible_distances) / 2))
        ]
        count = 0
    else:
        distances = [
            possible_distances[i]
            for i in range(0, int(len(possible_distances) / 2 + 1))
        ]
        count = -1
    distances = distances[::-1]
    for d in distances:
        if d > record_distance:
            count = count + 2
    return count


def calculate_counts_of_wins(times: List[int], distances: List[int]) -> List[int]:
    counts = []
    for record_time, record_distance in zip(times, distances):
        possible_distances = calculate_possible_distances(record_time)
        counts.append(ways_to_win(possible_distances, record_distance))
    return counts


if __name__ == "__main__":
    lines = read_input(Path("inputs/input.txt"))
    times = parse_line(lines[0])
    distances = parse_line(lines[1])
    counts_of_wins = calculate_counts_of_wins(times, distances)
    print(counts_of_wins[0])
