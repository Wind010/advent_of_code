'''
https://adventofcode.com/2024/day/18
'''


from collections import deque
import re
from common.common import arg_parse, assertions, timer
import heapq
import networkx as ntwx

DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

CORRUPTED_BYTE = '#'
STEP = 'O'
SPACE = '.'

# def parse_input(lines):
#     coords = []
#     max_x, max_y = 0, 0
#     for line in lines:
#         r, c = map(int, line.split(','))
#         if r > max_x:
#             max_x = r
#         if c > max_y:
#             max_y = c
#         coords.append((r, c))
#     return coords, max(max_x, max_y)
        

def print_grid(byte_positions, steps, size):
    for y in range(size):
        row = ''.join(f'{CORRUPTED_BYTE} ' if (x, y) in set(byte_positions)
                      else f'{STEP} ' if (x, y) in steps
                      else f'{SPACE} '
                      for x in range(size))
        print(row)



@timer
def find_min_steps_for_exit_bfs1(byte_positions, mem, size):
    start, end = (0, 0), (size, size)
    byte_positions = set(byte_positions[:mem])
    #print_grid(byte_positions, (), size)
    
    queue = deque([(0, 0, 0)])  # (x, y, steps)
    seen = {start}
    parent = {start: None}
    
    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == end:
            # Reconstruct the path
            path = []
            current = end
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()  # Reverse the path to get it from start to end
            return steps, path

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            
            # Check if the new position is in bounds and not visited.  Bug was size and not size+1
            if 0 <= nx <= size and 0 <= ny <= size and (nx, ny) not in byte_positions and (nx, ny) not in seen:
                seen.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny, steps + 1))
                
            # print_grid(byte_positions, (), size)
            
    return 0, []


@timer
def find_min_steps_for_exit_bfs2(byte_positions, mem, size):
    start, end = (0, 0), (size, size)
    byte_positions = set(byte_positions[:mem])
    queue = deque([start])
    seen = {start: 0}
    
    while queue:
        x, y = queue.popleft()
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if (nx, ny) in byte_positions:
                continue
            if nx < 0 or ny < 0 or nx > size or ny > size:
                continue
            if (nx, ny) in seen:
                continue
            
            seen[(nx, ny)] = seen[(x, y)] + 1
            
            queue.append((nx, ny))
            if (nx, ny) == end:
                return seen[(nx, ny)]
            
    return 0


@timer
def find_min_steps_for_exit_bisect(byte_positions, mem, size):
    def path(mem):
        seen = {*byte_positions[:mem]}
        queue = [(0, (0,0))]

        for dist, (x,y) in queue:
            if (x,y) == (size, size):
                return dist

            for x,y in (x,y+1), (x,y-1), (x+1,y), (x-1,y):
                if (x,y) not in seen and 0 <= x <= size and 0 <= y <= size:
                    queue.append((dist+1, (x,y)))  # Modify queue while iterating is intended.
                    seen.add((x,y))
        return 1e7

    return path(mem)


@timer
def find_min_steps_for_exit_networkx(byte_positions, mem, size):
    graph = ntwx.grid_2d_graph(size+1, size+1)

    for i, p in enumerate(byte_positions[:mem]):
        graph.remove_node(p)

    return ntwx.shortest_path_length(graph, (0, 0), (size, size))



def main(args, data):
    lines = data.strip().split('\n')
    
    byte_positions = [tuple(map(int, list(re.findall(r'\d+', coords)))) for coords in lines]
    mem, size = 1024, 70

    if len(byte_positions) == 25:
        mem, size = 12, 6

    min_steps1 = find_min_steps_for_exit_bfs1(byte_positions, mem, size)[0]
    min_steps2 = find_min_steps_for_exit_bfs2(byte_positions, mem, size)
    min_steps3 = find_min_steps_for_exit_networkx(byte_positions, mem, size)
    min_steps4 = find_min_steps_for_exit_bisect(byte_positions, mem, size)
    
    assert min_steps1 == min_steps2 == min_steps3 == min_steps4

    assertions(args, min_steps1, 22, 324, 304)
    return min_steps1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

