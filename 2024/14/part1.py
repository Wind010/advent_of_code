'''
https://adventofcode.com/2024/day/14
'''


from collections import defaultdict
import re
from common.common import arg_parse, assertions, timer


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
        
        
        
@timer
def find_saftey_factor(grid, steps):
    rows, cols = len(grid), len(grid[0])
    robots = parse_input(grid)
    # x, y
    
    r_pos = defaultdict(tuple)
    for step in steps:
        for i, robot in enumerate(robots):
            x, y, vx, vy = robot
            n_x, n_y = x + vx, y + vy
            
            if 0 <= n_x < rows and 0 <= n_y < cols:
                r_pos[i] = (n_x, n_y)
            else:
                r_pos[i] = (n_x % rows, n_y % cols)
                
        
        # TODO:  Determine quadrants based off mid points of rows and cols
    return r_pos


def main(args, data):
    lines = data.strip().split('\n')
 
    safety_factor = find_saftey_factor(lines, 1)
    

    return safety_factor
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

