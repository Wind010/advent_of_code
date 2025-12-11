'''
https://adventofcode.com/2025/day11
'''

# Looks like a graph problem where we would have to traverse every path 
# with DFS starting with "you" and ending with "out".

# Manually try this later, just use NetworkX for now.

from common.common import arg_parse, assertions, timer
import networkx as ntwx

def find_all_valid_paths(lines, source, target):
    G = ntwx.DiGraph()
    
    for line in lines:
        src, *dest = line.split()
        for node in dest:
            G.add_edge(src.strip(':'), node)
            
    # [G.add_edge(src.strip(':'), node) 
    #     for line in lines 
    #     for src, *dest in [line.split()] 
    #     for node in dest]
    
    return [*ntwx.all_simple_paths(G, source, target)]
    
    


def main(args, data):
    lines = data.strip().split('\n')
    
    total_paths = len(find_all_valid_paths(lines, 'you', 'out'))

    assertions(args, total_paths, 5, 701, 534)
    return total_paths
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

