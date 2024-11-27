'''
--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.
The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.
Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.
In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.
Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
'''


from collections import defaultdict
import re
from common.common import arg_parse

from part1 import MAP_NAMES

from multiprocessing import Pool
from dataclasses import *


# Brute Force

def get_seeds_initial(seeds):
    pairs = [*zip(seeds[::2], seeds[1::2])]
    return [[s for s in range(start, start + steps)] for start, steps in pairs]  # Out-Of-Memory Brah


def get_seeds_iterator(seeds):
    pairs = [*zip(seeds[::2], seeds[1::2])]
    for start, steps in pairs:
        for s in range(start, start + steps):
            yield s



def find_lowest_location_of_seeds_brute(lines):
    seeds = []
    pass


def get_maps_list(data):
    #return [[list(map(int, line.split(" "))) for line in sec.split("\n")[1::]] for sec in data.split("\n\n")[1::]]
    maps = []
    for cat in data.split("\n")[1::]:
        lines = cat.split("\n")
        m = []
        for line in lines[1::]:
            m.append(list(map(int, line.split(" "))))
        maps.append(m)
    
    return maps


def get_maps_dict(data):
    maps = defaultdict(list)
    for cat in data.split("\n\n")[1::]:
        lines = cat.split("\n")
        map_name = ''
        m = []
        for line in lines:
            if line == '':
                continue
            if any(c.isalpha() for c in line):
                map_name = line.split(' ')[0]
                continue
            m.append(list(map(int, line.split(" "))))
        maps[map_name].extend(m)

    return maps
    

def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')
    
    seed_integers = list(map(int, re.findall(r'\d+', lines[0])))
    #seeds = get_seeds_initial(seed_integers)
    seeds = get_seeds_iterator(seed_integers)
    maps = get_maps_list(data)
    
    maps = get_maps_dict(data)

    min_location = 10e12
    
    category_mapped_values = defaultdict(list)
    for seed in seeds:
        new_value = seed
        category_mapped_values['seeds'].append(new_value)
        for key, values in maps.items():
            for rule in values:
                dest_start, source_start, length = rule
                if source_start <= new_value and new_value < source_start + length:
                    new_value = new_value + dest_start - source_start
                    category_mapped_values[key].append(new_value)
                    #print(key, category)
                    break;
            else:
                category_mapped_values[key].append(new_value)
            continue
 
    min_location = min(category_mapped_values['humidity-to-location'])
    
    
 
    if 'input1.txt' in file_path: assert min_location == 46
    if 'input2.txt' in file_path: assert min_location == 462648396



if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)
