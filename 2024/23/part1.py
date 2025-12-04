'''
https://adventofcode.com/2024/day/23
'''


from itertools import combinations
import re
from common.common import arg_parse, assertions, timer
from collections import defaultdict
import networkx as ntwx


def parse_input(data):
    nodes, edges = set(), set()
    for line in data:
        parts = line.split("-")
        c1, c2 = parts[0], parts[1]
        nodes.add(c1)
        nodes.add(c2)
        edges.add((c1, c2))
        
    # [parts for line in data for parts in [line.split("-")] for c1, c2 in [parts] 
    #   for _ in (nodes.add(c1), nodes.add(c2), edges.add((c1, c2)))]
    return nodes, edges
    
    
def find_computer_groups(nodes, edges, group_size):
    groupings = []

    def has_edge(edges, n1, n2):
        return (n1, n2) in edges or (n2, n1) in edges
    
    def dfs(current_group, candidates, not_candidates):
        if len(current_group) >= group_size:
            groupings.append(current_group[:])
        
        for node in candidates:
            new_candidates = [c for c in candidates if has_edge(edges, node, c)]
            new_not_candidates = [c for c in not_candidates if has_edge(edges, node, c)]
            
            current_group.append(node)
            dfs(current_group, new_candidates, new_not_candidates)
            current_group.pop()
            not_candidates.append(node)
    
    nodes = list(nodes)
    for i in range(len(nodes)):
        dfs([nodes[i]], [n for n in nodes[i+1:] if has_edge(edges, nodes[i], n)], [])
    
    return groupings


@timer
def find_n_interconnected_computers_initial(data, n, starts_with):
    '''Takes too long'''
    nodes, edges = parse_input(data)

    groupings = find_computer_groups(nodes, edges, n)
    sets = set()
    
    for groups in groupings:
        for nodes in combinations(groups, n):
            if any(n[0] == starts_with for n in nodes):
                sets.add(tuple(sorted(nodes)))
    
    return len(sets)


def find_n_interconnected_computers_networkx(data, group_size, starts_with):
    G = ntwx.Graph()
    nodes, edges = parse_input(data)
    
    for edge in edges:
        G.add_edge(*edge)

    cliques = [c for c in ntwx.find_cliques(G) if len(c) >= group_size and any(n[0] == starts_with for n in c)]
    # sets = set()
    # for c in groups:
    #     for nodes in combinations(c, group_size):
    #         if any(n[0] == starts_with for n in nodes):
    #             sets.add(tuple(sorted(nodes)))
    
    sets = {
        tuple(sorted(nodes))
        for c in cliques
        for nodes in combinations(c, group_size)
        if any(n[0] == starts_with for n in nodes)
    }
    
    return len(sets)


def preprocess_graph(graph, min_clique_size):
    return {
        node: neighbors
        for node, neighbors in graph.items()
        if len(neighbors) >= min_clique_size - 1
    }

# Bron-Kerbosch Algorithm - https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def bron_kerbosch(graph, R, P, X, cliques, clique_size=None):
    if not P and not X:
        if clique_size and len(R) >= clique_size:
            cliques.append(R)
        return

    pivot = next(iter(P | X), None)
    if pivot:
        neighbors = graph[pivot]
    else:
        neighbors = set()

    for node in list(P - neighbors):
        bron_kerbosch(
            graph,
            R | {node},
            P & graph[node],
            X & graph[node],
            cliques,
            clique_size
        )
        P.remove(node)
        X.add(node)


def find_n_interconnected_computers_bron_kerbosch(data, group_size, starts_with):
    nodes, edges = parse_input(data)

    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    # nodes == graph.keys()

    graph = preprocess_graph(graph, group_size)

    cliques = []
    bron_kerbosch(graph, set(), set(nodes), set(), cliques, group_size)

    sets = set()
    for clique in cliques:
        if any(n[0] == starts_with for n in clique):
            for subset in combinations(clique, group_size):
                if any(n[0] == starts_with for n in subset):
                    sets.add(frozenset(subset))

    return len(sets)


def main(args, data):
    lines = data.strip().split('\n')
    
    #computer_sets1 = find_n_interconnected_computers_initial(lines, 3, 't')
    computer_sets2 = find_n_interconnected_computers_networkx(lines, 3, 't')
    computer_sets3 = find_n_interconnected_computers_bron_kerbosch(lines, 3, 't')
    
    assert computer_sets2 == computer_sets3

    assertions(args, computer_sets2, 7, 1046, 1358)
    return computer_sets2
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

