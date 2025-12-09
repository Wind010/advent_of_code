'''
https://adventofcode.com/2025/day8
'''

# Sounds like a graph problem.

# 1.	Read input to parse coordinates.
# 2.	Compute all pairwise distances with distance formla.
# 3.	Sort pairs by distance.
# 4.	Use Union-Find to connect the closest N pairs.
# 5.	Count the sizes of all resulting circuits.
# 6.	Multiply the sizes of the three largest circuits.

# This is essentially Kruskal's algorithm for building a minimum spanning forest,
# but you stop after a fixed number of edges/connections.

# I am too lazy to implement Union-Find from scratch, so I'll use NetworkX.
# TODO: Implement Union-Find manually

from common.common import arg_parse, assertions, timer

import math
import itertools
import networkx as ntwx


def parse_input(data):
    return  [
        tuple(map(int, line.strip().split(',')))
        for line in data.strip().splitlines()
        if line.strip()
    ]

@timer
def find_largest_circuits_networkx(coords, pairs=1000):
    n = len(coords)
    
    # Build all possible edges with distances
    edges = []
    for (i, a), (j, b) in itertools.combinations(enumerate(coords), 2):
        dist = math.dist(a, b)
        edges.append((i, j, dist))

    # Sort edges by distance and select the N shortest
    edges.sort(key=lambda x: x[2])
    selected_edges = edges[:pairs]

    # Build the graph with only the N shortest edges
    graph = ntwx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_weighted_edges_from(selected_edges)

    # Find connected components/circuits and their sizes
    connected_circuits = sorted([len(c) for c in ntwx.connected_components(graph)], reverse=True)
    
    return connected_circuits[:3]


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        if self.size[xr] < self.size[yr]:
            xr, yr = yr, xr
        self.parent[yr] = xr
        self.size[xr] += self.size[yr]
        return True

@timer
def find_largest_circuits_with_union_find(coords, pairs):
    n, edges = len(coords), []
    for (i, a), (j, b) in itertools.combinations(enumerate(coords), 2):
        dist = math.dist(a, b)
        edges.append((dist, i, j))
    edges.sort()  # This SOB took a while to find.

    # Connect the closest N pairs/edges/circuits

    # parent = list(range(n))
    # def find(x):
    #     while parent[x] != x:
    #         parent[x] = parent[parent[x]]
    #         x = parent[x]
    #     return x
    # def union(x, y):
    #     xr, yr = find(x), find(y)
    #     if xr == yr:
    #         return False
    #     parent[yr] = xr
    #     return True

    
    uf = UnionFind(n)

    # Process exactly circuits/edges, regardless of whether union is successful
    for dist, i, j in edges[:pairs]:
        uf.union(i, j)

    # Count circuit sizes
    circuit_sizes = {}
    for i in range(n):
        root = uf.find(i)
        circuit_sizes[root] = circuit_sizes.get(root, 0) + 1

    return sorted(circuit_sizes.values(), reverse=True)[:3]



def main(args, data):
    coords = parse_input(data)
    
    pairs = 1000 if len(coords) > 20 else 10
    largest_circuts1 = find_largest_circuits_networkx(coords, pairs)
    largest_circuts2 = find_largest_circuits_with_union_find(coords, pairs)
    
    product1 = math.prod(largest_circuts1)
    assertions(args, product1, 40, 54180, 330786)
    
    product2 = math.prod(largest_circuts2)
    assertions(args, product2, 40, 54180, 330786)

    return product2
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

