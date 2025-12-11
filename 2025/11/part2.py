'''
https://adventofcode.com/2025/day11
'''

# We can filter for paths that include 'dac' AND 'fft'.

from part1 import populate_graph
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



def find_all_relevant_paths_memo(G, node, dac_seen=None, fft_seen=None, memo=None):
    if memo is None:
        memo = {}
    
    cache_key = (node, dac_seen, fft_seen)
    
    if cache_key in memo:
        return memo[cache_key]
    
    if node == "out":
        # We have reached the end of path and we've either seen both or not.
        result = dac_seen and fft_seen
        memo[cache_key] = result
        return result
    
    dac_seen = dac_seen or node == "dac"
    fft_seen = fft_seen or node == "fft"
    
    result = sum(find_all_relevant_paths_memo(G, neighbor, dac_seen, fft_seen, memo)
                 for neighbor in G.neighbors(node))
    
    memo[cache_key] = result
    return result


@cache
def find_all_relevant_paths_cache(G, node, dac_seen=None, fft_seen=None):
    if node == "out":
        return dac_seen and fft_seen
    dac_seen = dac_seen or node == "dac"
    fft_seen = fft_seen or node == "fft"
    return sum(find_all_relevant_paths_cache(G, neighbor, dac_seen, fft_seen)
               for neighbor in G.neighbors(node))


def main(args, data):
    lines = data.strip().split('\n')
    #x = find_all_relevant_paths(lines, 'svr', 'out')
    G = populate_graph(lines)
    #total_paths = len(find_all_relevant_paths(G, 'svr', 'out'))
    total_paths = find_all_relevant_paths_memo(G, 'svr')


    assertions(args, total_paths, None, 390108778818526, 499645520864100, 2)
    return total_paths
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input4.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

