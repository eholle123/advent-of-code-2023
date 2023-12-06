from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint

Row = NewType("Row", List[int|str])
Coordinate = NewType("Coordinate", Tuple[int, int])

@dataclass
class Number:
    number_start_coordinate: Coordinate
    number: List[int]


integers = [i for i in range(0,10)]

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]

def make_row(line: str) -> List[int|str]:
    row = []
    for char in line:
        if try_parse_digit(char):
            row.append(try_parse_digit(char))
        else:
            row.append(char)
    return row

def try_parse_digit(s: str) -> Optional[int]:
    try:
        return int(s)
    except ValueError:
        return None

def special_char(char: str) -> bool:
    return not ((char == ".") or (char in integers))

def make_engine_schematic(lines: List[str]):
    engine_schematic = [make_row(line) for line in lines]
    return engine_schematic

def make_numbers(engine_schematic) -> List[Number]:
    numbers = []
    for row_num, row in enumerate(engine_schematic):
        while col_num in range(len(row)):
            entry = engine_schematic[row_num][col_num]
            if entry in integers:
                coordinate = Coordinate(row_num,col_num)
                number = make_number(coordinate, engine_schematic)
                numbers.append(number)
    return numbers

def make_number(coordinate: Coordinate, engine_schematic) -> Number:
    number_start_coordinate = Coordinate(row_num, col_num)
    number = []
    entry = engine_schematic[row_num][col_num]
    while entry in integers:
        number.append(entry)
        col_num = col_num + 1

if __name__ == "__main__":
    lines = read_input(Path("inputs/test_input_yields_4361.txt"))
    engine_schematic = make_engine_schematic(lines)
    make_numbers(engine_schematic)
    #pprint(engine_schematic)
