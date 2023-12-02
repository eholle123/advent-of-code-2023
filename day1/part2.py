from pathlib import Path
from typing import List, Optional

nums = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def parse_digits(line: str) -> List[int]:
    digits = []
    for index in range(len(line)):
        if digit := try_parse_digit(line[index]):
            digits.append(digit)
        else:
            for number in nums.keys():
                if line.startswith(number, index):
                    digits.append(nums[number])
    return digits


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
