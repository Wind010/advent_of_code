'''
https://adventofcode.com/2024/day/10
'''


from collections import defaultdict
from common.common import arg_parse, assertions, timer

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


def dfs(r, c, grid, visited, target, path, paths):
    if grid[r][c] == target:
        path.append((r, c))
        paths.append(list(path))
        return
    
    visited[r][c] = True
    path.append((r, c))
    
    for d_r, d_y in DIRECTIONS:
        n_r, n_c = r + d_r, c + d_y
        # Check if the new cell is within bounds, not visited, and has a value greater than the current cell by 1
        if is_in_bounds(n_r, n_c, grid) and grid[n_r][n_c] == grid[r][c] + 1:
            dfs(n_r, n_c, grid, visited, 9, path, paths)
    
    visited[r][c] = False
    path.pop()


@timer
def find_trailhead_paths_bfs(grid):
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



def bfs(start_row, start_col, grid):
    queue = [(start_row, start_col)]
    visited = set()
    
    path = []
    
    while queue:
        # Get the first element from the queue
        r, c = queue.pop(0)  # Use pop(0) for FIFO
        
        if (r, c) in visited:
            continue
        
        visited.add((r, c))
        
        if grid[r][c] == 9:
            path.append((r, c))
        
        # Checkout all valid neighboring cells
        for d_r, d_c in DIRECTIONS:
            n_r = r + d_r
            n_c = c + d_c
            
            # Check if the neighbor is within grid bounds
            if is_in_bounds(n_r, n_c, grid) and grid[n_r][n_c] == grid[r][c] + 1:
                    queue.append((n_r, n_c))
    
    return path

        

def main(args, data):
    num_grid = [[int(d) for d in line] for line in data.strip().split('\n')]
    
    paths = find_trailhead_paths_bfs(num_grid)

    scores = [len(p) for p in paths.values()]
    total_score = sum(scores)
    
    assertions(args, total_score, 36, 517)

    return total_score
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

