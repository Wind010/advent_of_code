'''
https://adventofcode.com/2024/day/16
'''



import re
from common.common import arg_parse, assertions, timer
from part1 import DIRECTIONS, parse_input_cleaner, dijkstra


@timer
def 

def main(args, data):
    lines = data.strip().split('\n')
    
    total = 0

    assertions(args, total, 9021, 1)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

