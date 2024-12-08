'''
https://adventofcode.com/2024/day/8

Description was terrible.  Go with the diagrams.  
Collinear:  Having both points through a straight line with the same distance in this case for the antinodes.
'''

import re

from collections import defaultdict
from itertools import combinations
from visualization import print_grid

# From CMDLINE
#import os, sys
#sys.path.insert(0, os.path.abspath('common'))
#from common import arg_parse, assertions, timer

from common.common import arg_parse, assertions, timer

def find_antennas(grid):
    ''' Time complexity:  O(n*m)'''
    antennas = defaultdict(list) # Every antenna frequency and list of corresponding coordinates.
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != '.':
                antennas[cell].append((r, c))
    #print(antennas)
    return antennas

# def find_antennas(grid):
#     return {cell: [(r, c) for c, cell in enumerate(row) if cell != '.']
#             for x, row in enumerate(grid) if any(cell != '.' for cell in row)}


@timer
def determine_antinodes_original(grid, antennas):
    ''' Time complexity:  O(n*m)'''
    rows, cols = len(grid), len(grid[0])
    antinodes = set()

    for freq, coords in antennas.items():
        for r, _ in enumerate(coords):
            for c in range(r + 1, len(coords)):
                diff = (coords[c][0] - coords[r][0], coords[c][1] - coords[r][1])
                
                # Determine antinodes for each pair of antenna positions
                pos1 = (coords[r][0] - diff[0], coords[r][1] - diff[1])
                if 0 <= pos1[0] < rows and 0 <= pos1[1] < cols:
                    antinodes.add(pos1)

                pos2 = (coords[c][0] + diff[0], coords[c][1] + diff[1])
                if 0 <= pos2[0] < rows and 0 <= pos2[1] < cols:
                    antinodes.add(pos2)

    return antinodes


@timer
def determine_antinodes_zip(grid, antennas):
    ''' Time complexity:  O(n*m*c) where c is the coordinates of found antennas'''
    rows, cols = len(grid), len(grid[0])
    antinodes = set()

    for freq, coords in antennas.items():
        for r, _ in enumerate(coords):
            for c in range(r + 1, len(coords)):
                diff = tuple(x - y for x, y in zip(coords[c], coords[r]))

                for i, direction in [(r, -1), (c, 1)]: # Check in both directions
                    pos = tuple([x + y * direction for x, y in zip(coords[i], diff)])
                    if 0 <= pos[0] < rows and 0 <= pos[1] < cols:
                        antinodes.add(pos)

    return antinodes


@timer
def determine_antinodes_combinations(grid, antennas):
    ''' 
    Time complexity:  O(n*m*c^2) where c is the coordinates of found antennas.
    The coordinates are pairs and we pair them
    '''
    rows, cols = len(grid), len(grid[0])
    antinodes = set()
    
    for freq, coords in antennas.items():
        # Generate pairs for each coordinate list for each anntenna frequency 
        # so the possitions of the antinodes can be calculated below.
        
        #print(coords)
        #print(list(combinations(coords, 2)))
        
        for (x1, y1), (x2, y2) in combinations(coords, 2):
            #print((x1, y1), (x2, y2))
            diff_x, diff_y = x2 - x1, y2 - y1

            pos1 = (x1 - diff_x, y1 - diff_y)
            pos2 = (x2 + diff_x, y2 + diff_y)

            for pos in (pos1, pos2):
                if 0 <= pos[0] < rows and 0 <= pos[1] < cols:
                    antinodes.add(pos)

    return antinodes

def main(args, data):
    grid = data.strip().split('\n')
    
    antennas = find_antennas(grid)
    
    antinodes1 = determine_antinodes_original(grid, antennas)
    antinodes2 = determine_antinodes_zip(grid, antennas)
    antinodes3 = determine_antinodes_combinations(grid, antennas)
    
    assert antinodes1 == antinodes2 == antinodes3
    
    print_grid(grid, antennas, antinodes1)
    total = len(antinodes1)
    
    assertions(args, total, 14, 332)

    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

