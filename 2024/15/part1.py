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

DIRECTIONS = {'^': (-1, 0), '>':(0, 1), 'v':(1, 0), '<':(0, -1)}



def print_grid(grid):
    rows, cols = len(grid), len(grid[0])
    print()
    for c in range(cols):
        cells = ''
        for r in range(rows):
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
    grid = move(grid, moves, robot)
    return grid


def move(grid, moves, robot):
    rows, cols = len(grid), len(grid[0])
    #print(grid, moves)
    
    queue = deque(robot)
    print_grid(grid)
    

    for m in moves:   
        x, y = robot
        dx, dy = DIRECTIONS[m]
        nx, ny = x + dx, y + dy
        can_move, movers = True, {}
        cell, next_cell = grid[x][y], grid[nx][ny]
        
        while nx > 0 and nx < rows-1 and ny > 0 and ny < cols-1:
            if next_cell == SPACE:
                # Normal move
                movers[(x + dx, y + dy)] = cell
                break
            elif next_cell == BOX:
                # Move box
                movers[(x + dx, y + dy)] = cell
                x += dx
                y += dy
            else:
                can_move = False
                break
            
        if can_move:
            for mx, my in movers:
                grid[mx][my] = movers[(mx, my)]
            x, y = robot
            robot = (nx, ny)
            grid[x][y] = SPACE
            #cell, next_cell = SPACE, ROBOT
            print_grid(grid)
    
    return grid
        


def main(args, data):
    lines = data.strip().split('\n')

    grid = find_box_gps_coordinates(lines)
    
    total_gps_coords = sum([x+100 * y for x, r in enumerate(grid) for y, c in enumerate(grid[0]) if grid[x][y] == BOX])
    


    assertions(args, total_gps_coords, 2416, 10092, 1, 2416)
    return total_gps_coords
    


if __name__ == "__main__":
    #args = arg_parse(__file__, 'input4.txt', main)
    args = arg_parse(__file__, 'input1.txt', main)
    #args = arg_parse(__file__, 'input2.txt', main)
    #args = arg_parse(__file__, 'input3.txt', main)

