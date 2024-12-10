'''
https://adventofcode.com/2024/day/10
'''


import re
from common.common import arg_parse, assertions, timer
from part1 import find_trail_heads, DIRECTIONS, is_in_bounds


 
def dfs(row, col, grid, visited):    
    if grid[row][col] == 9:
        return [(row, col)]

    if (row, col) in visited:
        return visited[(row, col)]

    paths = []
    for d_row, d_col in DIRECTIONS:
        n_r = row + d_row
        n_c = col + d_col

        if is_in_bounds(n_r, n_c, grid) and grid[n_r][n_c] == grid[row][col] + 1:
            paths.extend(dfs(n_r, n_c, grid, visited))

    visited[(row, col)] = paths  # Memoize the paths for current cell Pinky.
    
    return paths
    

def find_trailhead_paths_dfs(grid):
    trail_heads = find_trail_heads(grid)
    all_paths, visited = {}, {}

    for start_x, start_y in trail_heads:
        path = dfs(start_x, start_y, grid, visited)
        all_paths[(start_x, start_y)] = path
    
    return all_paths


def main(args, data):
    num_grid = [[int(d) for d in line] for line in data.strip().split('\n')]
    
    paths = find_trailhead_paths_dfs(num_grid)

    scores = [len(p) for p in paths.values()]
    total_score = sum(scores)
    
    assertions(args, total_score, 81, 1116)

    return total_score
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

