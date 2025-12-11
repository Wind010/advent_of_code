'''
https://adventofcode.com/2025/day11
'''

# We can filter for paths that include 'dac' AND 'fft'.

from common.common import arg_parse, assertions, timer
import networkx as ntwx

@timer
def find_all_relevant_paths(lines, source, target, nodes_to_include=['dac', 'fft']):
    G = ntwx.DiGraph()
    
    for line in lines:
        src, *dest = line.split()
        for node in dest:
            G.add_edge(src.strip(':'), node)
    
    return [path for path in ntwx.all_simple_paths(G, source, target)
            if all(node in path for node in nodes_to_include)]

# Takes too long.  Need to optimize with memoization possibly.



def main(args, data):
    lines = data.strip().split('\n')
    #x = find_all_relevant_paths(lines, 'svr', 'out')
    total_paths = len(find_all_relevant_paths(lines, 'svr', 'out'))


    assertions(args, total_paths, 1, 1, 1, 2)
    return total_paths
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input4.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

