from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint


@dataclass
class Range_Map:
    destination_start: int
    source_start: int
    range_length: int


@dataclass
class Map:
    map_name: "str"
    range_maps: List[Range_Map]


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def remove_blanks(lines: List[str]) -> List[str]:
    return [line for line in lines if line]


def parse_range_map(line: str) -> Range_Map:
    [d_start, s_start, r_length] = parse_numbers(line, False)
    return Range_Map(
        destination_start=d_start, source_start=s_start, range_length=r_length
    )


def parse_numbers(numbers_text: str, seed: Optional[bool]) -> List[int]:
    numbers = []
    nums_text = (numbers_text.lstrip()).split(" ")
    if seed == True:
        nums_text = nums_text[1:]
    for number_text in nums_text:
        if (number_text.strip() == "") is False:
            number = int(number_text.strip())
            numbers.append(number)
    return numbers


def parse_seed_ranges(line: str) -> List[Tuple[int,int]]:
    parsed_seeds = parse_numbers(line, True)
    seed_ranges = make_seed_range_tuple(parsed_seeds)
    return seed_ranges

def make_seed_range_tuple(parsed_seeds: List[int]) -> List[Tuple[int,int]]:
    seed_range_tuples = []
    for i in range(0,(len(parsed_seeds)),2): 
        seed_range_tuples.append(tuple([parsed_seeds[i],parsed_seeds[i+1]]))
    return seed_range_tuples

def seed_range_to_seeds(seed_range: Tuple[int,int]) -> List[int]:
    return [seed for seed in range(seed_range[0],(seed_range[0]+seed_range[1]))]

def parse_maps_data(lines: List[str]) -> List[Map]:
    maps = []
    i = 0
    for line in lines:
        if ":" in line:
            range_maps = []
            i = i + 1
            while i < len(lines):
                if ":" in lines[i]:
                    break
                else:
                    range_maps.append(parse_range_map(lines[i]))
                i = i + 1
            maps.append(Map(map_name=line, range_maps=range_maps))
    return maps


def map_source_to_destination(seed: int, range_maps: List[Range_Map]) -> int:
    mapped_seed = seed
    for range_map in range_maps:
        source_start = int(range_map.source_start)
        source_max = source_start + int(range_map.range_length)
        destination_start = int(range_map.destination_start)
        destination_max = destination_start + int(range_map.range_length)
        if seed in range(source_start, source_max):
            mapped_seed = destination_max - (source_max - seed - 1) - 1
    return mapped_seed


def map_sources_to_destinations(seeds: List[int], list_of_maps: List[Map]) -> List[int]:
    for mapper in list_of_maps:
        mapped_seeds = []
        for seed in seeds:
            mapped_seed = map_source_to_destination(seed, mapper.range_maps)
            mapped_seeds.append(mapped_seed)
        seeds = mapped_seeds
    return seeds


if __name__ == "__main__":
    lines = remove_blanks(read_input(Path("inputs/input.txt")))
    list_of_maps = parse_maps_data(lines[1:])
    seed_group1 = parse_seed_ranges(lines[0])
    seeds_groups = []
    for seed_range in parse_seed_ranges(lines[0]):
        seed_group1 = seed_range_to_seeds(seed_range)
        print(seed_group1)
        break
    #     seeds_groups.append(seed_range_to_seeds(seed_range))
    # for seeds_group in seeds_groups:
    #     map_seeds_to_locations = map_sources_to_destinations(seeds_group, list_of_maps)
    #     print(map_seeds_to_locations)
    # pprint(list_of_maps)
    # pprint(seeds)
    # pprint(min(map_seeds_to_locations))
