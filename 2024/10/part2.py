'''
https://adventofcode.com/2024/day/10
'''


import re
from common.common import arg_parse, assertions, timer
from part1 import find_trail_heads, DIRECTIONS, is_in_bounds
from collections import deque


def bfs(start_row, start_col, grid):
    queue = deque([(start_row, start_col)])
    visited, paths = set(), []
    
    while queue:
        row, col = queue.popleft()

        if grid[row][col] == 9:
            paths.append((row, col))
            continue

        if (row, col) in visited:
            continue

        visited.add((row, col))

        for d_row, d_col in DIRECTIONS:
            n_r = row + d_row
            n_c = col + d_col

            if is_in_bounds(n_r, n_c, grid) and grid[n_r][n_c] == grid[row][col] + 1:
                queue.append((n_r, n_c))

    return paths

 
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
    
    
@timer
def find_trailhead_paths_bfs(grid):
    '''
    Time complexity:  O(n*m).
    Space complexity: O(n*m)
    '''
    trail_heads = find_trail_heads(grid)
    all_paths = {}

    for start_x, start_y in trail_heads:
        path = bfs(start_x, start_y, grid)
        all_paths[(start_x, start_y)] = path
    
    return all_paths


@timer
def find_trailhead_paths_dfs(grid):
    '''
    Time complexity:  O(n*m).
    Space complexity: O(n*m)
    '''
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
    total_score1 = sum(scores)
    
    paths2 = find_trailhead_paths_dfs(num_grid)
    scores2 = [len(p) for p in paths2.values()]
    total_score2 = sum(scores2)
    
    assert total_score1 == total_score2
    
    assertions(args, total_score1, 81, 1116)

    return total_score1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

