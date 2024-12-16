'''
https://adventofcode.com/2024/day/15
'''



import re
from common.common import arg_parse, assertions, timer
from collections import deque



ROBOT = '@'
BOX = 'O'
WALL = '#'
SPACE = '.'

#DIRECTIONS = {'<': (-1, 0), 'v':(0, 1), '>':(1, 0), '^':(0, -1)}
DIRECTIONS = { "^": (-1, 0),"v": (1, 0),"<": (0, -1),">": (0, 1) }


def print_grid(grid):
    rows, cols = len(grid), len(grid[0])
    print()
    for r in range(rows):
        cells = ''
        for c in range(cols):
            cells += grid[r][c]
        print(cells)
    print()


def parse_input(lines):
    grid, moves, robot = [], [], None
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == ROBOT:
                robot = (row, col)
                
        if WALL in line:
            grid.append(list(line))
        else:
            moves.extend(line)
        
    #grid = [list(line) for line in lines if WALL in line]
    #moves = [c for line in lines if WALL not in line for c in line]
    #robot = find_robot_coordinates(lines)
    
    return grid, moves, robot


def find_robot_coordinates(lines):
    robot = None
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == ROBOT:
                robot = (row, col)
                break

    #robot_coords = [(row, col) for row, line in enumerate(lines) for col, c in enumerate(line) if c == ROBOT]
    #robot = robot_coords[0] if robot_coords else None
    return robot
    

@timer
def find_box_gps_coordinates(lines):
    grid, moves, robot = parse_input(lines)
    grid = push_it(grid, moves, robot)
    return grid


def push_it_original(grid, moves, robot):
    rows, cols = len(grid), len(grid[0])
    #print(grid, moves)
    
    queue = deque(robot)
    print_grid(grid)
    
    for m in moves:
        x, y = robot
        dx, dy = DIRECTIONS[m]
        #nx, ny = x + dx, y + dy
        can_move, pending = True, {}
        
        while True: #nx > 0 and nx < rows-1 and ny > 0 and ny < cols-1:
            nx, ny = x + dx, y + dy
            if grid[nx][ny] == SPACE:
                # Normal move
                pending[(nx, ny)] = grid[x][y]
                break
            elif grid[nx][ny] == BOX:
                # Move box
                pending[(nx, ny)] = grid[x][y]
                x, y = nx, ny
            else:
                can_move = False
                break
        
        if can_move:
            for mx, my in pending:
                grid[mx][my] = pending[(mx, my)]
                #print_grid(grid)
 
            
            #if nx > 0 and nx < rows-1 and ny > 0 and ny < cols-1:
            grid[x][y] = SPACE
            grid[nx][ny] = ROBOT
            #grid[nx][ny] = ROBOT

            #print(m)
            #print_grid(grid)
     
    return grid
        


@timer
def push_it(grid, moves, robot):
    r, c = robot
    for i, m in enumerate(moves):
        dr, dc = DIRECTIONS[m]
        nr, nc = r+ dr, c + dc

        while grid[nr][nc] not in [SPACE, WALL]:
            nr, nc = nr + dr, nc + dc

        if grid[nr][nc] == WALL:
            # Wall, no move
            #print(moves[i-1], m)
            #print_grid(grid)
            continue

        # Adjust robot positions and corresponding next cells.
        x, y = nr, nc
        while (x, y) != (r, c):
            x, y = x-dr, y-dc
            grid[nr][nc] = grid[x][y]
            nr, nc = nr-dr, nc-dc
        
        grid[x][y] = SPACE
        r, c = r + dr, c + dc
        
        #print(moves[i-1], m)
        #print_grid(grid)
        
    return grid



def main(args, data):
    lines = data.strip().split('\n')

    grid = find_box_gps_coordinates(lines)
    total_gps_coords = sum([100* x + y for x, r in enumerate(grid) for y, c in enumerate(grid[0]) if grid[x][y] == BOX])
    
    assertions(args, total_gps_coords, 10092, 1515788, 1437174, 2028)
    
    return total_gps_coords
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input4.txt', main)
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

