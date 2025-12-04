'''
https://adventofcode.com/2024/day/23
'''


from collections import defaultdict
import re
from common.common import arg_parse, assertions, timer
from part1 import parse_input
import networkx as ntwx


def find_largest_clique_password_networkx(data):
    nodes, edges = parse_input(data)
    G = ntwx.Graph()

    for edge in edges:
        G.add_edge(*edge)

    cliques = list(ntwx.find_cliques(G))
    #print(sorted(cliques, key=len, reverse=True))
    maximal_clique = sorted(sorted(cliques, key=len, reverse=True)[0])

    return ','.join(maximal_clique)


def bron_kerbosch(graph, r, p, x, cliques):
    if not p and not x:
        cliques.append(r)
    else:
        for v in list(p):
            # Inline pivot
            bron_kerbosch(graph, r | {v}, p & graph[v], x & graph[v], cliques)
            p.remove(v)
            x.add(v)


def find_largest_clique_password_bron_kerbosch(data):
    nodes, edges = parse_input(data)
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    cliques = []
    bron_kerbosch(graph, set(), set(nodes), set(), cliques)
    maximal_clique = sorted(sorted(cliques, key=len, reverse=True)[0])
    
    return ','.join(maximal_clique)


def main(args, data):
    lines = data.strip().split('\n')
    
    #password = find_largest_clique_password_networkx(lines)
    password = find_largest_clique_password_bron_kerbosch(lines)


    assertions(args, password, "co,de,ka,ta", "de,id,ke,ls,po,sn,tf,tl,tm,uj,un,xw,yz"
               , "cl,ei,fd,hc,ib,kq,kv,ky,rv,vf,wk,yx,zf")
    return password
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)


