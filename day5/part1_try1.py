from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint


# @dataclass
# class Range:
#     destination_start: int
#     source_start: int 
#     r_length: int

@dataclass
class Map:
    map_name:'str'
    range_map: Dict[int,int]



# source_num: int
# destination_num: int
# Map = Dict['source_num': 'destination_num',
#               'source_num1': 'destination_num'
#               ...]
# List_of_Maps = ['str', List[Map]]


def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]

def remove_blanks(lines: List[str]) -> List[str]:
    return [line for line in lines if line]

def parse_seeds(line: str) -> List[int]:
    return parse_numbers(line, True)

def parse_maps_data(lines: List[str]) -> List[Map]:
    maps = []
    i = 1
    for line in lines:
        # print(':' in lines[i])
        if ':' in line:
            range_map = {}
            i = i + 1
            while i < len(lines):
                if ':' in lines[i]:
                    break
                else:
                    range_map.update(parse_range_map(lines[i]))
                # print(range_map)
                i = i + 1
            maps.append(Map(map_name=line, range_map=range_map))
        # print(maps)
    return maps


def parse_range_map(line: str) -> Dict[int,int]:
    range_map = {}
    # numbers = []
    # for number_text in line.split(" "):
    #     if ((number_text.strip()) == "") is False:
    #         numbers.append(int(number_text.strip()))
    # pprint(parse_numbers(line))
    [destination_start, source_start, r_length] = parse_numbers(line, False)
    source_range = range(source_start,source_start+r_length)
    destination_range = range(destination_start,destination_start+r_length)
    range_map.update({source:destination for (source,destination) in zip(source_range,destination_range)})
    return range_map


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


def map_source_to_destination(seed: int, range_map: Dict[int,int]) -> int:
    if range_map.get(seed):
        mapped_seed = range_map[seed]
    else:
        mapped_seed = seed
    return mapped_seed


def map_sources_to_destinations(seeds: List[int], list_of_maps: List[Map]) -> List[int]:
    for mapper in list_of_maps:
        mapped_seeds = []
        for seed in seeds:
            mapped_seed = map_source_to_destination(seed, mapper.range_map)
            mapped_seeds.append(mapped_seed)
        seeds = mapped_seeds
    return seeds


if __name__ == "__main__":
    lines = remove_blanks(read_input(Path("inputs/test_input_yields_35.txt")))
    list_of_maps = parse_maps_data(lines[1:])
    seeds = parse_seeds(lines[0])
    map_seeds_to_locations = map_sources_to_destinations(seeds, list_of_maps)
    pprint(min(map_seeds_to_locations))
    
