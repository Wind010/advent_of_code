'''
https://adventofcode.com/2024/day/6
'''


from common.common import arg_parse, assertions, timer
import sys
import multiprocessing
GUARD = '^'
OBSTACLE = '#'


# def find_guard_initial_position(grid):
#     for r, _ in enumerate(grid):
#         for c, _ in enumerate(grid[0]):
#             #print(r, c, grid[r][c])

#             if grid[r][c] == GUARD:
#                 #print(r, c, grid[r][c])
#                 return r, c
#     raise ValueError(f"Starting position for the guard {GUARD} was not found in the grid.")



# def get_obstacle_cells(grid):
#     return [(r, c) for r, _ in enumerate(grid) for c, __ in enumerate(grid[0]) if grid[r][c] == OBSTACLE]


def find_guard_and_obstacles(grid):
    '''
    Time complexity of O(n*m)
    '''
    guard_position, obstacles = None, []

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == GUARD:
                guard_position = (r, c)
            elif cell == OBSTACLE:
                obstacles.append((r, c))
    
    if guard_position is None:
        raise ValueError(f"Starting position for the guard ({GUARD}) was not found in the grid.")
    
    return guard_position, obstacles


def start(grid, guard_pos, obs_pos):
    '''
    Time complexity of O(n*m) in the worst case.
    '''
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
    r, c = guard_pos
    o_row, o_col = obs_pos
    visited_cells = set()
    direction = 0  # Initial direction is up.
    
    while True:
        visited_cells.add((r, c))

        # Calculate next position
        dr, dc = directions[direction]
        next_row, next_col = r + dr, c + dc

        # Check if out of bounds or hitting the blocking point
        if not (0 <= next_row < rows and 0 <= next_col < cols):
            if grid[o_row][o_col] == OBSTACLE:
                return visited_cells # Can save memory if needed by returning the length of the set.
            break
        if grid[next_row][next_col] == OBSTACLE or (next_row, next_col) == (o_row, o_col):
            # Turn right
            direction = (direction + 1) % len(directions) # Take the modulus of 4.
        else:
            # Move to the next cell
            r, c = next_row, next_col

    return len(visited_cells)



@timer
def monitor_guard_path(grid):
    '''
    Time complexity of O(n*m*o) where o is number of obstacles.
    '''
    guard_pos, obstacles = find_guard_and_obstacles(grid)

    total_steps = 0
    for pos in obstacles:
        steps = start(grid, guard_pos, pos)
        #print(steps)
        total_steps = max(total_steps, len(steps))
    
    return total_steps


@timer
def monitor_guard_path_multiprocesses(grid):
    '''
    Cuts time in about half...
    '''
    guard_pos, obstacles = find_guard_and_obstacles(grid)
    
    #from concurrent.futures import ProcessPoolExecutor
    #with ProcessPoolExecutor() as executor:
    
    # Tweaked
    with multiprocessing.Pool(processes=multiprocessing.cpu_count() // 2) as pool:
        # Maps each obstacle to the worker process
        all_paths = pool.starmap(start, [(grid, guard_pos, obstacle) for obstacle in obstacles])
        #print(all_paths)
    
    return len(max(all_paths))


def start_wrapper(args):
    grid, start_row, start_col, block_row, block_col = args
    return start(grid, start_row, start_col, block_row, block_col)



def main(args, data):
    grid = data.strip().split('\n')

    total_steps = monitor_guard_path_multiprocesses(grid)
    
    assertions(args, total_steps, 41, 4789)
    
    return total_steps


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
