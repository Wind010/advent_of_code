'''
https://adventofcode.com/2025/day12
'''



import re
from common.common import arg_parse, assertions, timer


def main(args, data):
    lines = data.strip().split('\n')
    
    total = 0

    assertions(args, total, 1, 1)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

