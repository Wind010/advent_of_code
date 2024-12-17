'''
https://adventofcode.com/2024/day/16
'''



import re
from common.common import arg_parse, assertions, timer
import heapq
import math

START = 'S'
END = 'E'
OBSTACLE = '#'

DIRECTIONS = {'^': (-1, 0), 'v': (1, 0), '<': (0, 1), '>': (0, -1)}


def parse_input(lines):
    grid = [list(line.strip()) for line in lines]
    start, end = None, None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == START:
                start = (r, c)
            elif ch == END:
                end = (r, c)
    return grid, start, end


def parse_input_cleaner(lines):
    grid = [list(line.strip()) for line in lines]
    positions = {
        ch: (r, c)
        for r, row in enumerate(grid)
        for c, ch in enumerate(row)
        if ch in START + END
    }
    s, e = positions.get(START), positions.get(END)
    
    return grid, s, e

@timer
def find_shortest_path_dijkstra(lines):
    grid, (sr, sc), (er, ec) = parse_input(lines)
    dist = dijkstra(grid, [(sr, sc, "<")])
    best = 10e10
    for d in "^v<>":
        if (er, ec, d) in dist:
            best = min(best, dist[(er, ec, d)])
    return best

@timer
def find_shortest_path_a_star(lines):
    grid, (sr, sc), (er, ec) = parse_input(lines)
    dist = a_star(grid, [(sr, sc, "<")], (er, ec))
    best = 10e10
    for d in "^v<>":
        if (er, ec, d) in dist:
            best = min(best, dist[(er, ec, d)])
    return best


def dijkstra(grid, start):
    '''
    Time complexity:  O(n*log*n) since we check each we check O(4*m) for each possible traversal cell
    and the priority queue/heap is O(N*logN).
    Space complexity: O(n)
    '''
    
    distance, pq = {}, []
    
    for sr, sc, direction in start:
        distance[(sr, sc, direction)] = 0
        heapq.heappush(pq, (0, sr, sc, direction))

    while pq:
        (dist, r, c, direction) = heapq.heappop(pq)
        
        if distance[(r, c, direction)] < dist:
            # Skip if a shorter path to this state has already been found
            continue
        
        # Find all directional neighbors
        for next_dir in "^v<>".replace(direction, ''):
            if (r, c, next_dir) not in distance or distance[
                (r, c, next_dir)
            ] > dist + 1000:
                distance[(r, c, next_dir)] = dist + 1000
                heapq.heappush(pq, (dist + 1000, r, c, next_dir))
                
        dr, dc = DIRECTIONS[direction]
        nr, nc = r + dr, c + dc # Move
        
        # Check if the neighbor is within bounds and not an obstacle
        if (0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != OBSTACLE
                and ((nr, nc, direction) not in distance or distance[(nr, nc, direction)] > dist + 1)):
            distance[(nr, nc, direction)] = dist + 1
            heapq.heappush(pq, (dist + 1, nr, nc, direction))

    return distance



def a_star(grid, start, end):
    '''
    A* search algorithm.  INCOMPLETE
    Time complexity: 
    Space complexity: O(n)
    '''
    
    distance, pq = {}, []
    came_from = {}  # To reconstruct the path
    
    def heuristic(a, b):
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    for sr, sc, direction in start:
        distance[(sr, sc, direction)] = 0
        heapq.heappush(pq, (0, sr, sc, direction))
        came_from[(sr, sc, direction)] = None

    while pq:
        (f, r, c, direction) = heapq.heappop(pq)
        
        # If we reach the goal, reconstruct the path
        if (r, c) == end:
            current = (r, c, direction)
            while current in came_from:
                current = came_from[current]
                
            return distance
        
        if distance[(r, c, direction)] < f:
            # Skip if a shorter path to this state has already been found
            continue
        
        # Find all directional neighbors
        for next_dir in "^v<>".replace(direction, ''):
            if (r, c, next_dir) not in distance or distance[
                (r, c, next_dir)
            ] > distance[(r, c, direction)] + 1000:
                distance[(r, c, next_dir)] = distance[(r, c, direction)] + 1000
                priority = distance[(r, c, next_dir)] + heuristic((r, c), end)
                heapq.heappush(pq, (priority, r, c, next_dir))
                came_from[(r, c, next_dir)] = (r, c, direction)
                
        dr, dc = DIRECTIONS[direction]
        nr, nc = r + dr, c + dc  # Move
        
        # Check if the neighbor is within bounds and not an obstacle
        if (0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != OBSTACLE
                and ((nr, nc, direction) not in distance or distance[(nr, nc, direction)] > distance[(r, c, direction)] + 1)):
            distance[(nr, nc, direction)] = distance[(r, c, direction)] + 1
            priority = distance[(nr, nc, direction)] + heuristic((nr, nc), end)
            heapq.heappush(pq, (priority, nr, nc, direction))
            came_from[(nr, nc, direction)] = (r, c, direction)

    return distance



def main(args, data):
    lines = data.strip().split('\n')
    
    score = find_shortest_path_dijkstra(lines)
    score2 = find_shortest_path_a_star(lines)
    
    assert score == score2
    
    assertions(args, score, 7036, 11048, 83432, 105508)
    return score
    

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input4.txt', main)

