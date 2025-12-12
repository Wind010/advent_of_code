'''
https://adventofcode.com/2025/day12
'''

# Sounds like Tetris and we to see if all the specified shapes fit the W x H area without overlapping.
# We can try brute forcing all placements with all rotations of each of the specified shape for each area.
# Probably will work for part1, but not for part2.

import re
from common.common import arg_parse, assertions, timer



def main(args, data):
    lines = data.strip().split('\n')

    assertions(args, total, 3, 557, 505)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

