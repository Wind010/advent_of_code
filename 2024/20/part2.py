'''
https://adventofcode.com/2024/day/20
'''



import re
from common.common import arg_parse, assertions, timer
from part1 import find_cheats_under_n_picoseconds

def main(args, data):
    lines = data.strip().split('\n')
    
    pico_seconds = 100
    if len(lines) == 15:
        pico_seconds = 20

    
    cheats1 = sum(find_cheats_under_n_picoseconds(lines, pico_seconds, 20))
    #cheats2 = sum(find_cheats_under_n_picoseconds_dijkstra(lines, pico_seconds, 20))
    #cheats3 = sum(find_cheats_under_n_picoseconds_combo(lines, pico_seconds, 2))

    #assert cheats2 == cheats3
    
    assertions(args, cheats1, 31, 999556, 1010263)
    return cheats1


if __name__ == "__main__":
    #args = arg_parse(__file__, 'input1.txt', main)
    #args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
