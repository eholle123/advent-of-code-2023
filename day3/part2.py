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


Gears = NewType("Gears", Dict[Tuple[int, int], List[int]])


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


def get_gears(schematic: Schematic) -> Gears:
    gears = {}
    for symbol_position in schematic.symbols.keys():
        rows = range(symbol_position[0] - 1, symbol_position[0] + 2)
        cols = range(symbol_position[1] - 1, symbol_position[1] + 2)
        symbol_buffer = [position for position in itertools.product(rows, cols)]
        gear_numbers = []
        for number in schematic.numbers:
            if is_number_touching_gear(number, symbol_buffer):
                gear_numbers.append(number.value)
        if len(gear_numbers) == 2:
            gears[symbol_position] = gear_numbers
    return Gears(gears)


def is_number_touching_gear(
    number: SchematicNumber, symbol_buffer: List[Tuple[int, int]]
) -> bool:
    number_positions = [
        number_position
        for number_position in itertools.product(
            [number.row], [col for col in range(number.col, number.col + number.length)]
        )
    ]
    for number_position in number_positions:
        if number_position in symbol_buffer:
            return True
    return False


if __name__ == "__main__":
    # lines = read_input(Path("inputs/test_input_yields_4361.txt"))
    lines = read_input(Path("inputs/input.txt"))
    # pprint(lines)
    # print()

    schematic = parse_schematic(lines)
    # pprint(schematic)

    gears = get_gears(schematic)
    # print(gears)

    result = 0
    for gear in gears.keys():
        result += gears[gear][0] * gears[gear][1]
    print(result)
