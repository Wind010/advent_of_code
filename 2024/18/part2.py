'''
https://adventofcode.com/2024/day/18
'''




import re
from common.common import arg_parse, assertions, timer
from part1 import print_grid, find_min_steps_for_exit_bfs1, find_min_steps_for_exit_bisect 
import networkx as nx
from bisect import bisect


@timer
def find_first_corrupted_blocking_cell_bfs_binary_search(byte_positions, size):
    
    # low could be zero, but we know at 1024 corrupted bytes, it's not blocked.
    low, high = 1024, len(byte_positions)
    while high - low > 1:
        new_mem = (low + high) // 2
        if find_min_steps_for_exit_bfs1(byte_positions, new_mem, size):
            low = new_mem
        else: 
            high = new_mem
    return byte_positions[low]
    

@timer
def find_first_corrupted_blocking_cell_networkx(byte_positions, size):
    graph = nx.grid_2d_graph(size+1, size+1)

    # Slow and can be optimized if we use BFS.
    for i, p in enumerate(byte_positions):
        graph.remove_node(p)
        if not nx.has_path(graph, (0, 0), (size, size)):
            return f"{p[0]},{p[1]}"
    return '0,0'


@timer
def find_first_corrupted_blocking_cell_bisect(byte_positions, size):
    # Credit to 4HbQ

    def bfs(mem):
        seen = {*byte_positions[:mem]}
        #seen = set(byte_positions[:mem])
        queue = [(0, (0,0))]

        for dist, (x,y) in queue:
            if (x,y) == (size, size): return dist
            for dx,dy in (x,y+1), (x,y-1), (x+1,y), (x-1,y):
                if (dx,dy) not in seen and 0 <= x < size+1 and 0 <= y < size+1:
                    queue.append((dist+1, (dx,dy)))
                    seen.add((dx,dy))
        return 1e9
    
    # We create a list of distance/steps returned from bfs based off corrupted byte positions.
    # We return 77777 if there is no 
    #[bfs(b) for b in range(1024, len(byte_positions))]
    
    print(bfs(1024))
    
    v = bisect(range(1024, len(byte_positions)), 1e9-1, key=bfs)
    return byte_positions[bisect(range(1024, len(byte_positions)), 77776, key=bfs) - 1]




# TODO:  A-Star



def main(args, data):
    lines = data.strip().split('\n')
    
    #x(lines)
    
    #byte_positions = [tuple(map(int, list(re.findall(r'\d+', coords)))) for coords in lines]
    byte_positions = [*map(eval, lines)]
    size = 70
    
    if len(byte_positions) == 25:
        size = 6

    #min_steps1 = find_first_corrupted_blocking_cell_bfs_binary_search(lines, size)
    min_steps2 = find_first_corrupted_blocking_cell_bisect(lines, size)
    #min_steps3 = find_first_corrupted_blocking_cell_networkx(byte_positions, size)
    
    assertions(args, min_steps2, '2,0', '46,23', '50,28')
    return min_steps2
    


if __name__ == "__main__":
    #args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

