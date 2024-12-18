
'''
https://adventofcode.com/2024/day/15
'''



from collections import deque
import re
from common.common import arg_parse, assertions, timer
from part1 import BOX as OLDBOX, SPACE, WALL, ROBOT, DIRECTIONS, parse_input, print_grid


BOX = "[]"
MAPPINGS = {WALL: WALL + WALL, OLDBOX: BOX, SPACE: "..", ROBOT: ROBOT + SPACE}



@timer
def find_boxes_gps_coordinates(lines):
    grid, moves, robot = parse_input(lines)
    robot = (robot[0], robot[1] * 2)
    
    grid = [list("".join(MAPPINGS[c] for c in line)) for line in grid] # Resize the warehouse/grid
    
    gg = {(x , y): grid[y][x] for x, col in enumerate(grid[0]) for y, row in enumerate(grid)}
    
    print(gg)
    grid = push_it(grid, moves, robot)
    return grid



def push_it(grid, moves, robot):
    r, c = robot
    print_grid(grid)
    for i, m in enumerate(moves):
        dr, dc = DIRECTIONS[m]

        to_move, queue, handled, can_move = [], deque([(r, c)]), set(), True
        while queue:
            x, y = queue.popleft()
            if (x, y) in handled:
                continue
            
            handled.add((x, y))
            nr, nc = x + dr, y + dc

            next_cell = grid[nr][nc]
            if next_cell == WALL:
                can_move = False
                break

            to_move.append((x, y, nr, nc))
            if next_cell == SPACE:
                continue

            box_check_queue = deque([(nr, nc)])
            if dc == 0:
                if next_cell == BOX[0]:
                    box_check_queue.append((nr + 1, nc))
                elif next_cell == BOX[1]:
                    box_check_queue.append((nr - 1, nc))

        if can_move:
            while to_move:
                print_grid(grid)
                x, y, nr, nc = to_move.pop()
                grid[nr][nc] = grid[x][y]
                grid[x][y] = SPACE
                print_grid(grid)

            r, c = r + dr, c + dc

    print_grid(grid)

    return grid






def main(args, data):
    lines = data.strip().split('\n')
    # and grid[x][y] == BOX[1]]
    grid = find_boxes_gps_coordinates(lines)
    total_gps_coords = sum([100 * x + y for x, r in enumerate(grid) 
                            for y, c in enumerate(grid[0]) if grid[x][y-1] == BOX[0]])

    assertions(args, total_gps_coords, 1, 1, 1, 1, 9021)
    return total_gps_coords
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input5.txt', main)
    #args = arg_parse(__file__, 'input2.txt', main)

