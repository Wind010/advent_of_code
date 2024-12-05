'''
https://adventofcode.com/2024/day/3
'''


import re
from common.common import arg_parse, timer, assertions


def main(args, data):
    lines = data.strip().split('\n')
    
    #matches = re.findall( r'mul\(\d+,\d+\)', line)
    multi_pair = [(int(a) * int(b)) for line in lines 
                  for a, b in re.findall(r'mul\((\d+),(\d+)\)', line)]

    total = sum(multi_pair)
    
    print(total)

    assertions(args, total, 161, 187833789)
    
    return total


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

