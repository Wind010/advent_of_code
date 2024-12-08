'''
https://adventofcode.com/2024/day/8
'''



import re
from common.common import arg_parse, assertions, timer
from collections import defaultdict


def find_antennas(grid):
    antennas = defaultdict(list)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != '.':
                antennas[cell].append((r, c))
    return antennas

# def find_antennas(grid):
#     return {cell: [(r, c) for c, cell in enumerate(row) if cell != '.']
#             for x, row in enumerate(grid) if any(cell != '.' for cell in row)}

def check_if_matching_antenna(grid, antenna):
    rows, cols = len(grid), len(grid[0])
    
    row, col = antenna
    m1_row = row + 2
    m1_col = col + 1
    
    m2_row = row - 2
    m2_col = row + 1
    
    matches = []
    
    if 0 <= m1_row < rows and 0 <= m1_col < cols:
        match1 = grid[m1_row][m1_col]
        match2 = grid[m2_row][m2_col]
        print(f"Searching for match {grid[row][col]}")
        
        if match1 == grid[row][col]:
            print(f"Found matching antenna of {grid[row][col]} at {match1} at ({m1_row}, {m1_col})")
            matches.append((False, m1_row, m1_col))
    
        if match2 == grid[row][col]:
            print(f"Found matching antenna of {grid[row][col]} at {match2} at ({m2_row}, {m2_col})")
            matches.append((True, m2_row, m2_col))
    
    return matches



def determine_antinodes(grid, antennas):
    antinodes, grid_height = set(), len(grid)
    grid_width = len(grid[0]) if grid_height > 0 else 0
    
    for freq, aantenna_positions in antennas.items():
        for i, pos in enumerate(aantenna_positions):
            for match in check_if_matching_antenna(grid, pos):
                isRight, r, c = match
                if isRight:
                    antinodes.add((r + 2, c + 1))
                else:
                    antinodes.add((r - 2, c + 1))
            
    return list(antinodes)


def determine_antinodes2(grid, antennas):
    rows, cols = len(grid), len(grid[0])
    antinodes = set()

    for freq, coords in antennas.items():
        for r in range(len(coords)):
            for c in range(r + 1, len(coords)):
                diff = (coords[c][0] - coords[r][0], coords[c][1] - coords[r][1])

                pos1 = (coords[r][0] - diff[0], coords[r][1] - diff[1])
                if 0 <= pos1[0] < rows and 0 <= pos1[1] < cols:
                    antinodes.add(pos1)

                pos2 = (coords[c][0] + diff[0], coords[c][1] + diff[1])
                if 0 <= pos2[0] < rows and 0 <= pos2[1] < cols:
                    antinodes.add(pos2)

    return antinodes



def print_grid(grid, antennas, antinodes):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            is_antenna = False
            is_antinode = False
            for frequency, antenna_locations in antennas.items():
                if (x, y) in antenna_locations:
                    print(frequency, end='')
                    is_antenna = True
                    break
            if (y, x) in antinodes:
                is_antinode = True
            if not is_antenna and not is_antinode:
                print('.', end='')
            elif is_antinode:
                print('#', end='')
        print()



def main(args, data):
    grid = data.strip().split('\n')

    # Find all antennas
    antennas = find_antennas(grid)

    
    #antinodes = determine_antinodes(grid, antennas)
    antinodes = determine_antinodes2(grid, antennas)
    
    print_grid(grid, antennas, antinodes)
    
    total = len(antinodes)
    
    assertions(args, total, 14, 332)

    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

