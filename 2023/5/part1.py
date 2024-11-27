'''
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.
"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.
"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.
"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"
You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."
The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.
The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.
Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.
Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.
The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.
Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.
So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
'''


import re
from common.common import arg_parse
from collections import *

MAP_NAMES = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light'
             , 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']

def get_map_initial(lines):
    maps = {}
    for line in lines:
        if line == '':
            break
        
        parts = [*map(int, line.split(" "))]
        for i in range(parts[2]):
            dest, source = parts[0] + i, parts[1] + i
            maps[source] = dest

    return maps

def get_map_dict_comp(lines):
    maps = {}
    for line in lines:
        if line == '' or any(c.isalpha() for c in line):
            break

        dest_start, source_start, length = map(int, line.split())
        maps.update({source_start + i: dest_start + i for i in range(length)})

    return maps

def get_map_tuples(lines):
    maps = []
    for line in lines:
        if line == '' or any(c.isalpha() for c in line):
            break
        
        dest_start, source_start, length = map(int, line.split())
        maps.append((dest_start, source_start, length))
        
    return maps


def map_values_to_list(values, lines):
    for i, line in enumerate(lines[1::]):
        for name in MAP_NAMES:
            if line.startswith(name):
                mapper = get_map_initial(lines[i+2::]) # lines[i+1:][:2] or lines[i+1:i+3]
                values = [mapper[c] if c in mapper else c for c in values]
    return values

#
def map_values_to_dict(lines):
    maps = {}
    for i, line in enumerate(lines[1::]):
        for name in MAP_NAMES:
            if line.startswith(name):
                mapper = get_map_tuples(lines[i+2::])  # lines[i+2:][:2] or lines[i+2:i+3]
                maps[name] = mapper
                # [(50, 98, 2), (52, 50, 48)]
    return maps

# TODO:  Use generators to just get last min.
def process_maps_mem_efficient(seeds, lines):
    maps = map_values_to_dict(lines)
    mapped_values = defaultdict(list)
    for seed in seeds:
        new_value = seed
        mapped_values['seeds'].append(new_value)
        for key, values in maps.items():
            for rule in values:
                dest_start, source_start, length = rule

                if source_start <= new_value and new_value < source_start + length:
                    new_value = new_value + dest_start - source_start
                    mapped_values[key].append(new_value)
                    print(key, new_value)
                    break;
            else:
                mapped_values[key].append(new_value)
            continue

    return mapped_values


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')

    seeds = map(int, re.findall(r'\d+', lines[0]))
    categories = process_maps_mem_efficient(seeds, lines[1::])

    min_location = min(categories['humidity-to-location'])
    print(categories, min_location)
                
    if 'input1.txt' in file_path: assert min_location == 35
    if 'input2.txt' in file_path: assert min_location == 462648396

            

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)
