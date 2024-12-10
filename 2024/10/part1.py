'''
https://adventofcode.com/2024/day/10
'''


from collections import defaultdict
from common.common import arg_parse, assertions, timer
from collections import deque

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_trail_heads(grid):
    ''' Time complexity:  O(n*m)'''
    trail_heads = set()
    for r, row in enumerate(grid):
        for c, cell in enumerate(map(int, row)):
            if cell == 0:
                trail_heads.add((r, c))
    #print(trail_heads)
    return trail_heads


def is_in_bounds(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def dfs_stack(start_row, start_col, grid):
    stack = [(start_row, start_col)]
    visited = set()
    path = []

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        
        visited.add((r, c))

        if grid[r][c] == 9:
            path.append((r, c))

        for d_r, d_c in DIRECTIONS:
            n_r, n_c = r + d_r, c + d_c
            
            if is_in_bounds(n_r, n_c, grid) and grid[n_r][n_c] == grid[r][c] + 1:
                stack.append((n_r, n_c))
    
    return path



def dfs_recursive(row, col, grid, visited, path):
    if (row, col) in visited or not is_in_bounds(row, col, grid):
        return

    visited.add((row, col))
    
    if grid[row][col] == 9:
        path.append((row, col))
    
    for d_r, d_c in DIRECTIONS:
        n_r, n_c = row + d_r, col + d_c
        
        if is_in_bounds(n_r, n_c, grid) and grid[n_r][n_c] == grid[row][col] + 1:
            dfs_recursive(n_r, n_c, grid, visited, path)


@timer
def find_trailhead_paths_dfs_recursive(grid):
    trail_heads = find_trail_heads(grid)
    all_paths = {}
    
    for start_x, start_y in trail_heads:
        visited = set()
        path = []
        dfs_recursive(start_x, start_y, grid, visited, path)
        all_paths[(start_x, start_y)] = path
    
    return all_paths


@timer
def find_trailhead_paths_dfs_stack(grid):
    trail_heads = find_trail_heads(grid)
    all_paths = {}

    for start_x, start_y in trail_heads:
        path = dfs_stack(start_x, start_y, grid)
        all_paths[(start_x, start_y)] = path

    return all_paths


def bfs(start_row, start_col, grid):
    # Use deque since can append elements at the end in O(1), but removing elements from the 
    # begining requires shifting all remaining elements to the left, which is O(n).
    queue = deque([(start_row, start_col)])
    visited, path = set(), []
    
    while queue:
        r, c = queue.pop()
        
        if (r, c) in visited:
            continue
        
        visited.add((r, c))
        
        if grid[r][c] == 9:
            path.append((r, c))

        for d_r, d_c in DIRECTIONS:
            n_r = r + d_r
            n_c = c + d_c
            
            # Check if the neighbor is within grid bounds
            if is_in_bounds(n_r, n_c, grid) and grid[n_r][n_c] == grid[r][c] + 1:
                    queue.append((n_r, n_c))
    
    return path


@timer
def find_trailhead_paths_bfs(grid):
    '''
    Time complexity:  O(n*m).
    Space complexity: O(n*m)
    '''
    rows, cols = len(grid), len(grid[0])
    trail_heads = find_trail_heads(grid)
    all_paths = {}
 
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    for start_x, start_y in trail_heads:
        path = bfs(start_x, start_y, grid)
        all_paths[(start_x, start_y)] = path
        
        if not visited[start_x][start_y]:
            path = []
            #dfs(start_x, start_y, grid, visited, 9, path, all_paths)
            #all_paths[(start_x, start_y)] = path
            
    return all_paths



def main(args, data):
    num_grid = [[int(d) for d in line] for line in data.strip().split('\n')]
    
    paths1 = find_trailhead_paths_bfs(num_grid)
    scores1 = [len(p) for p in paths1.values()]
    total_score1 = sum(scores1)
    
    paths2 = find_trailhead_paths_dfs_stack(num_grid)
    scores2 = [len(p) for p in paths2.values()]
    total_score2 = sum(scores2)
    
    paths3 = find_trailhead_paths_dfs_recursive(num_grid)
    scores3 = [len(p) for p in paths3.values()]
    total_score3 = sum(scores3)
    
    assert total_score1 == total_score2 == total_score3
    
    assertions(args, total_score1, 36, 517)

    return total_score1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

