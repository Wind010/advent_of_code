'''
https://adventofcode.com/2025/day4
'''

from common.common import arg_parse, assertions, timer, DIRECTIONS_8


def check_neighbor_rolls(row, col, grid):
    count = 0
    for dr, dc in DIRECTIONS_8:
        r, c = row + dr, col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == "@":
                count += 1
    return count

def get_accessible_rolls(grid):
    score = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "@":
                if check_neighbor_rolls(row, col, grid) < 4:
                    score += 1
    return score


def main(args, data):
    lines = data.strip().split('\n')
    total = get_accessible_rolls(lines)
    assertions(args, total, 13, 1578, 1578)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)


