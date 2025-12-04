'''
https://adventofcode.com/2025/day1
'''

from common.common import arg_parse, assertions, time
from functools import cache

LIMIT = 99
INIT_POS = 50

def turn_safe_initial(data):
    pos = INIT_POS
    count = 0
    for d in data:
        dir = -1 if d[0] == 'L' else 1
        steps = int(d[1:])
        
        #print(pos, steps, dir, count)
        for i in range(steps):
            if pos == 0:
                count += 1
            
            if pos == LIMIT and dir == 1:
                pos = 0
            elif pos == 0 and dir == -1:
                #print(i, pos, steps, dir, count)
                pos = LIMIT
            else:
                pos += dir
           #print(i, pos, steps, dir, count)
    
    return count

def main(args, data):
    lines = data.strip().split('\n')
    zeros_count = turn_safe_initial(lines)
    assertions(args, zeros_count, 6, 6858, 6689)


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

