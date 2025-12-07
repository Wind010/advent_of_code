'''
https://adventofcode.com/2025/day7
'''

from part1 import find_splits
from common.common import arg_parse, assertions, timer


def main(args, data):
    splits, total = find_splits(data)
    
    assertions(args, total, 40, 390684413472684, 18818811755665)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)


