'''
https://adventofcode.com/2024/day/14
'''


from collections import defaultdict
import re
from common.common import arg_parse, assertions, timer
from collections import deque
import math

WIDTH = 101
HEIGHT = 103
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def parse_input(lines):
    robots = [
        (int(px), int(py), int(vx), int(vy))
        for line in lines
        for px, py, vx, vy in [re.findall(r'-?\d+', line)]
    ]
        
    # return (
    #     [(int(a), int(b)) for a, b in re.findall(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', '\n'.join(lines))],
    #     [(int(c), int(d)) for c, d in re.findall(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', '\n'.join(lines))][1::2]
    # )
    return robots
        


def determine_quadrant(x, y, width, height):
    mid_x, mid_y = width // 2, height // 2
    
    # return (1 if x < mid_x else 2) + (2 if y >= mid_y else 0)
    # return (int(x > mid_x)) + (int(y > mid_y) * 2)
    if x < mid_x:
        return 1 if y < mid_y else 3
    else:
        return 2 if y < mid_y else 4


@timer
def find_saftey_factor_clean(grid, steps):
    robots = parse_input(grid)

    width, height = WIDTH, HEIGHT
    if len(robots) == 12:
        width, height = 11, 7

    positions = defaultdict(list)
    quadrants = [0, 0, 0, 0]
    for i, robot in enumerate(robots):
        x, y, vx, vy = robot
        x = (x + steps * (vx + width)) % width
        y = (y + steps * (vy + height)) % height

        positions[robot].append((x, y))
        
        mid_x, mid_y = width // 2, height // 2
        if x == mid_x or y == mid_y:
            continue
        
        # From above breakdown.
        j = (int(x > mid_x)) + (int(y > mid_y) * 2)
        quadrants[j] += 1

    #print(positions)
    #return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
    return math.prod(quadrants)


 
def main(args, data):
    lines = data.strip().split('\n')
 
    safety_factor1 = find_saftey_factor_clean(lines, 100)
    
    assertions(args, safety_factor1, 12, 219512160, 218965032)

    return safety_factor1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

