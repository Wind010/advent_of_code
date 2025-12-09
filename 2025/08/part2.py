'''
https://adventofcode.com/2025/day8
'''

# 1.	Read input to parse coordinates.
# 2.	Compute all pairwise distances with distance formla.
# 3.    Sort pairs by distance, this time ascending.
# 4.	Use Union-Find (Disjoint Set) to connect the closest N pairs/cicuits.
# 5.	Iterate through the pairs and if not connected, connect them via union.  Track the last pair and stop when all connected.
# 6.	Multiply the x-coordinats of the last pair connected.


# I am too lazy to implement Union-Find from scratch, so I'll use NetworkX.
# TODO: Implement Union-Find manually

from part1 import parse_input, UnionFind
from common.common import arg_parse, assertions, timer

import math
import itertools
import networkx as ntwx

@timer
def find_last_connection_product_networkx(coords):
    n, edges = len(coords), []
    
    for (i, a), (j, b) in itertools.combinations(enumerate(coords), 2):
        dist = math.dist(a, b)
        edges.append((dist, i, j))
    edges.sort()

    graph = ntwx.Graph()
    graph.add_nodes_from(range(n))

    last_edge = None
    for dist, i, j in edges:
        graph.add_edge(i, j, weight=dist)
        if ntwx.number_connected_components(graph) == 1:
            last_edge = (i, j)
            break

    x1 = coords[last_edge[0]][0]
    x2 = coords[last_edge[1]][0]
    return x1 * x2

@timer
def find_last_connection_product_with_union_find(coords):
    n = len(coords)
    edges = []
    for (i, a), (j, b) in itertools.combinations(enumerate(coords), 2):
        dist = math.dist(a, b)
        edges.append((dist, i, j))
    edges.sort()

    uf = UnionFind(n)
    components = n
    last_pair = None
    for dist, i, j in edges:
        if uf.union(i, j):
            components -= 1
            last_pair = (i, j)
            if components == 1:
                break
            
    x1 = coords[last_pair[0]][0]
    x2 = coords[last_pair[1]][0]
    return x1 * x2



def main(args, data):
    coords = parse_input(data)
    
    product1 = find_last_connection_product_networkx(coords)
    assertions(args, product1, 25272, 25325968, 3276581616)

    product2 = find_last_connection_product_with_union_find(coords)
    assertions(args, product2, 25272, 25325968, 3276581616)

    return product2
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

