'''
https://adventofcode.com/2025/day4
'''

from common.common import arg_parse, assertions, timer
from part1 import check_neighbor_rolls


def get_accessible_rolls(grid):
    prev, score = -1, 0
    while prev != score:
        prev = score
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "@":
                    if check_neighbor_rolls(row, col, grid) < 4:
                        score += 1
                        grid[row][col] = "X"
    return score
    
    

def main(args, data):
    lines = [list(line) for line in data.strip().split('\n')]
    total = get_accessible_rolls(lines) 
    assertions(args, total, 43, 10132, 10132)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)


