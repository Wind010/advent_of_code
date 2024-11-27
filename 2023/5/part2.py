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


import math
import re
from common.common import arg_parse
from collections import defaultdict
from part1 import map_values_mem_efficient, get_map_tuples, MAP_NAMES

from multiprocessing import Pool
from dataclasses import *



# Brute Force, Parallel Reverse Lookup, Split Ranges

@dataclass
class Range:
    start: int
    length: int
    # def __init__(self, start, length):
    #     self.start = start
    #     self.length = length
        
    def contains(self, value: int) -> bool:
        return self.start <= value < self.start + self.length


def generate_range(pair):
    start, steps = pair
    return [s for s in range(start, start + steps)]

# def get_map_tuples(lines):
#     maps = []
#     for line in lines:    
#         if line == '':
#             break
        
#         dest_start, source_start, length = map(int, line.split())
#         maps.append(Range(dest_start, length), source_start)
        
#     return maps

def contains_range(location, seed_ranges, maps):
    loc = location
    for m in maps:
        for dest_start, source_start, length in m:
            r = Range(dest_start, length)
            if r.contains(loc):
                loc = loc + dest_start - source_start
                break

    return loc if any(r.contains(loc) for r in seed_ranges) else None


def get_seeds_initial(seeds):
    pairs = [*zip(seeds[::2], seeds[1::2])]
    return [[s for s in range(start, start + steps)] for start, steps in pairs]  # Out-Of-Memory Brah


def get_seeds_yield(seeds):
    pairs = [*zip(seeds[::2], seeds[1::2])]
    for start, steps in pairs:
        for s in range(start, start + steps):
            yield s
            

def get_seed_ranges(seeds):
    return [Range(*pair) for pair in [*zip(seeds[::2], seeds[1::2])]]
 
 
def find_lowest_location_of_seeds_brute(lines):
    seeds = []
    pass
    


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')
    

    seed_integers = list(map(int, re.findall(r'\d+', lines[0])))
    #seeds = get_seeds_initial(seed_integers)
    seed_ranges = get_seed_ranges(seed_integers)
 
    maps = []
    for line in lines[1:]:
        trg_start, src_start, length = map(int, line.split(" "))
        m.append((Range(trg_start, length), src_start))

    maps.append(m)


    maps = maps[::-1] # Go from locations checking intervals/ranges all the way up to initial seed ranges.

    for loc in range(int(1e9)):
        result = contains_range(loc, seed_ranges, maps)
        if result is not None:
            print(result)
            return
        
        

    # with Pool(15) as pool:
    #     for loc in pool.imap(contains_range, range(int(1e9)), int(1e6))):
    #         if loc is not None:
    #             print(loc)
    #             return


    min_location = math.inf

    categories = defaultdict(list)
    for start, steps in pairs:
        for seed in range(start, start+steps):
            with Pool(15) as p:
                categories = p.imap(map_values_mem_efficient, [seed], lines[1::])
                #categories = map_to_category_mem_efficient([seed], lines[1::])

                # for r in categories:
                #     print(r)
                min_loc = min(categories['humidity-to-location'])
                min_location = min(min_loc, min_location)





    # min_location = min(categories['humidity-to-location'])
    # print(categories, min_location)

    if 'input1.txt' in file_path: assert min_location == 46
    if 'input2.txt' in file_path: assert min_location == 462648396



if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    # args = arg_parse(__file__, 'input2.txt', main)
    # main(args.file_path)
