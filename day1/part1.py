from pathlib import Path
from typing import List, Optional


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_digits(line: str) -> List[int]:
    # This was the first approach, but the := operator is cooler.
    # return [int(c) for c in line if try_parse_digit(c) is not None]
    return [digit for c in line if (digit := try_parse_digit(c))]


def try_parse_digit(s: str) -> Optional[int]:
    try:
        return int(s)
    except ValueError:
        return None


def get_calibration_value(digits: List[int]) -> int:
    digit1 = digits[0]
    digit2 = digits[-1]
    calibration_value = int(f"{digit1}{digit2}")
    return calibration_value


if __name__ == "__main__":
    lines = read_input(Path("inputs/input.txt"))
    calibration_values = [get_calibration_value(parse_digits(line)) for line in lines]
    sum_calibration_values = sum(calibration_values)
    print(sum_calibration_values)
