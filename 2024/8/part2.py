'''
https://adventofcode.com/2024/day/8
'''


import re
from common.common import arg_parse, assertions, timer
from collections import defaultdict
from part1 import find_antennas
from itertools import combinations
from visualization import print_grid


def determine_antinodes_original(grid, antennas):
    rows, cols = len(grid), len(grid[0])
    antinodes = set()

    for freq, coords in antennas.items():
        for r, _ in enumerate(coords):
            for c in range(r + 1, len(coords)):
                x1, y1 = coords[r]
                x2, y2 = coords[c]
                dx, dy = x2 - x1, y2 - y1

                # Positive direction from (x1, y1) to (x2, y2)
                x, y = x1, y1
                while 0 <= x < rows and 0 <= y < cols:
                    antinodes.add((x, y))
                    x += dx
                    y += dy

                # Negative direction from (x2, y2) to (x1, y1)
                x, y = x2, y2
                while 0 <= x < rows and 0 <= y < cols:
                    antinodes.add((x, y))
                    x -= dx
                    y -= dy

                # Could make in_bounds function check.
    return antinodes


@timer
def determine_antinodes_cleaner(grid, antennas):
    rows, cols = len(grid), len(grid[0])
    antinodes = set()
    
    for freq, coords in antennas.items():
        for i, _ in enumerate(coords):
            for j in range(i + 1,  len(coords)):
                x1, y1 = coords[i]
                x2, y2 = coords[j]
                dx, dy = x2 - x1, y2 - y1
                
                for d, direction in [(i, 1), (j, -1)]:
                    #print(d, direction)
                    x, y = coords[d]
                    while 0 <= x < rows and 0 <= y < cols:
                        antinodes.add((x, y))
                        x += dx * direction
                        y += dy * direction

    return antinodes


@timer
def determine_antinodes_zip(grid, antennas):
    rows, cols = len(grid), len(grid[0])
    antinodes = set()

    for freq, coords in antennas.items():
        for i, _ in enumerate(coords):
            for j in range(i + 1, len(coords)):
                diff = tuple(x - y for x, y in zip(coords[j], coords[i]))

                for d, direction in [(i, -1), (j, 1)]:
                    pos = coords[d]
                    while 0 <= pos[0] < rows and 0 <= pos[1] < cols:
                        antinodes.add(pos)
                        pos = tuple([x + y * direction for x, y in zip(pos, diff)])

    return antinodes


@timer
def determine_antinodes_combinations(grid, antennas):
    '''
    All possible pairs of positions from the list of positions
    '''
    rows, cols = len(grid), len(grid[0])
    antinodes = set()

    for freq, coords in antennas.items():
        
        for (x1, y1), (x2, y2) in combinations(coords, 2):
            dx, dy = x2 - x1, y2 - y1

            for i, direction in [(0, 1), (1, -1)]:
                x, y = (x1, y1) if i == 0 else (x2, y2)
                while 0 <= x < rows and 0 <= y < cols:
                    antinodes.add((x, y))
                    x += dx * direction
                    y += dy * direction

    return antinodes



def main(args, data):
    grid = data.strip().split('\n')
    antennas = find_antennas(grid)

    antinodes1 = determine_antinodes_original(grid, antennas)
    antinodes2 = determine_antinodes_cleaner(grid, antennas)
    antinodes3 = determine_antinodes_zip(grid, antennas)
    antinodes4 = determine_antinodes_combinations(grid, antennas)
    
    assert antinodes1 == antinodes2 == antinodes3 == antinodes4
    
    print_grid(grid, antennas, antinodes1)
    
    total = len(antinodes3)
    
    assertions(args, total, 34, 1174)

    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

