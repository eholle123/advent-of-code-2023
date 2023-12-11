import itertools
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint

# SCREAMING_SNAKE_CASE for module variables, available to everything in this file
DOTS_PATTERN = re.compile(r"(\.+)")
NUMBER_PATTERN = re.compile(r"(\d+)")


@dataclass
class SchematicNumber:
    value: int
    row: int
    col: int
    length: int


@dataclass
class Schematic:
    numbers: List[SchematicNumber]
    symbols: Dict[Tuple[int, int], str]


@dataclass
class Dots:
    """
    Intermediate data from parsing line.
    """

    length: int


@dataclass
class Number:
    """
    Intermediate data from parsing line.
    """

    value: str
    length: int


@dataclass
class Symbol:
    """
    Intermediate data from parsing line.
    """

    symbol: str


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_line(line: str) -> List[Dots | Number | Symbol]:
    parsed_line = []
    while len(line) > 0:
        if m := NUMBER_PATTERN.match(line):
            parsed_line.append(Number(value=m.groups()[0], length=m.end()))
            line = line[m.end() :]
        elif m := DOTS_PATTERN.match(line):
            parsed_line.append(Dots(length=m.end()))
            line = line[m.end() :]
        else:
            parsed_line.append(Symbol(symbol=line[0]))
            line = line[1:]
    return parsed_line


def parse_schematic(lines: List[str]) -> Schematic:
    numbers = []
    symbols = {}
    for row, line in enumerate(lines):
        col = 0
        for item in parse_line(line):
            if isinstance(item, Dots):
                col += item.length
            if isinstance(item, Number):
                numbers.append(
                    SchematicNumber(
                        value=int(item.value), row=row, col=col, length=item.length
                    )
                )
                col += item.length
            if isinstance(item, Symbol):
                symbols[(row, col)] = item.symbol
                col += 1
    return Schematic(numbers=numbers, symbols=symbols)


def sum_part_numbers(schematic: Schematic) -> int:
    result = 0
    for number in schematic.numbers:
        rows = range(number.row - 1, number.row + 2)
        cols = range(number.col - 1, number.col + number.length + 1)
        # itertools.product() gives Cartesian product
        if any(
            [
                schematic.symbols.get(position)
                for position in itertools.product(rows, cols)
            ]
        ):
            result += number.value
    return result


if __name__ == "__main__":
    # lines = read_input(Path("inputs/test_input_yields_4361.txt"))
    lines = read_input(Path("inputs/input.txt"))
    # pprint(lines)
    # print()

    schematic = parse_schematic(lines)
    # pprint(schematic)

    sum_important_numbers = sum_part_numbers(schematic)
    print(sum_important_numbers)
