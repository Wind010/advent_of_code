'''
https://adventofcode.com/2024/day/18
'''



import re
from common.common import arg_parse, assertions, timer
import networkx as nx


@timer
def find_min_steps_for_exit_networkx(byte_positions, mem, size):
    graph = nx.grid_2d_graph(size+1, size+1)

    for i, p in enumerate(byte_positions[:mem]):
        graph.remove_node(p)
        if not nx.has_path(graph, (0, 0), (size, size)):
            return p
    return 0


def main(args, data):
    lines = data.strip().split('\n')
    
    byte_positions = [tuple(map(int, list(re.findall(r'\d+', coords)))) for coords in lines]
    mem, size = 1024, 70

    if len(byte_positions) == 25:
        mem, size = 12, 6

    min_steps = find_min_steps_for_exit_networkx(byte_positions, mem, size)
    
    assertions(args, min_steps, 1, 1, 1)
    return min_steps
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

