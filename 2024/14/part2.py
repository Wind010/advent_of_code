'''
https://adventofcode.com/2024/day/14
'''

from collections import defaultdict
import re
from common.common import arg_parse, assertions, timer
from part1 import parse_input, WIDTH, HEIGHT



def print_grid(height, width, coords):
    for r in range(height):
        for c in range(width):
            if (r, c) in coords:
                print('#', end=' ')
            else:
                print('.', end=' ')
        print()


@timer
def find_tree_formation_interval(grid):
    robots = parse_input(grid)

    # Test data does not form the X-MAS tree.
    #positions = defaultdict(set)
    t, limit = 0, 10000
    while t < limit:
        t += 1
        positions = set()
        found = True
        for i, robot in enumerate(robots):
            x, y, vx, vy = robot
            x = (x + t * (vx + WIDTH)) % WIDTH
            y = (y + t * (vy + HEIGHT)) % HEIGHT
            if (x, y) in positions:
                found = False
                break
            
            #positions[robot].add((x, y))
            positions.add((x, y))
            print_grid(HEIGHT, WIDTH, positions)
            # It's any robot.  They're not statically in place.  So go by position in one set.
        
        if found:
            return t


def main(args, data):
    lines = data.strip().split('\n')
 
    seconds = find_tree_formation_interval(lines)
    
    assertions(args, seconds, 0, 6398, 7037)

    return seconds
    
    
if __name__ == "__main__":
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
