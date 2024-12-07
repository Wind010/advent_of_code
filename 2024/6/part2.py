'''
https://adventofcode.com/2024/day/6
'''


from common.common import arg_parse, assertions, timer
from part1 import find_guard_and_obstacles
import multiprocessing
from multiprocessing import Pool, cpu_count


@timer
def find_optimal_obstruction_positions(grid, guard_pos):
    '''
    Time complexity of O(n*m) in the worst case.
    '''
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
    total_positions_seen = 0

    for row in range(rows):
        for col in range(cols):
            r, c = guard_pos
            direction = 0  # Start facing up
            seen_states = set()

            while True:
                state = (r, c, direction)
                if state in seen_states:
                    total_positions_seen += 1
                    break
                seen_states.add(state)

                dr, dc = directions[direction]
                next_row = r + dr
                next_col = c + dc

                if not (0 <= next_row < rows and 0 <= next_col < cols):
                    break

                if grid[next_row][next_col] == '#' or (next_row == row and next_col == col):
                    direction = (direction + 1) % len(directions)
                else:
                    r, c = next_row, next_col

    return total_positions_seen


def process_position(o_row, o_col, grid, guard_pos, directions):
    '''
    Process a single starting position (o_row, o_col) and calculate the number of positions seen.
    '''
    rows, cols = len(grid), len(grid[0])
    r, c = guard_pos
    cur_dir = 0  # Start facing up
    seen_states, total_positions_seen= set(), 0

    while True:
        state = (r, c, cur_dir)
        #state = hash(state)
        if state in seen_states:
            total_positions_seen += 1
            break
        seen_states.add(state)

        dr, dc = directions[cur_dir]
        next_row = r + dr
        next_col = c + dc

        if not (0 <= next_row < rows and 0 <= next_col < cols):
            break

        if grid[next_row][next_col] == '#' or (next_row == o_row and next_col == o_col):
            cur_dir = (cur_dir + 1) % len(directions)
        else:
            r, c = next_row, next_col

    return total_positions_seen


@timer
def find_optimal_obstruction_positions_multiprocess(grid, guard_pos):
    '''
    Time complexity of O(n*m) in the worst case, improved using multiprocessing.
    '''
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    with Pool(processes=cpu_count() // 2) as pool:
        tasks = [(r, c, grid, guard_pos, directions) for r in range(rows) for c in range(cols)]
        result = pool.starmap(process_position, tasks)

    return sum(result)

    

def main(args, data):
    grid = data.strip().split('\n')
    guard_pos, obstacles = find_guard_and_obstacles(grid)

    #total_steps = find_optimal_obstruction_positions(grid, guard_pos)
    total_steps = find_optimal_obstruction_positions_multiprocess(grid, guard_pos)
    
    assertions(args, total_steps, 6, 1304)

 
    return total_steps
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

