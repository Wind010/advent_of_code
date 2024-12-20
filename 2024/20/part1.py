'''
https://adventofcode.com/2024/day/20
'''


from functools import cache
import re
from common.common import arg_parse, assertions, timer, DIRECTIONS
from collections import deque
import heapq
from itertools import combinations


OBSTACLE = '#'
START = 'S'
END = 'E'


def parse_input(lines):
    grid, start, end, walls = {}, (), (), set()
    for r, _ in enumerate(lines):
        for c in range(len(lines[0])):
            coords, v = (r, c), lines[r][c]
            grid[(r, c)] = v
            if v == START:
                start = coords
            elif v == END:
                end = coords
            elif v == OBSTACLE:
                walls.add(coords)
    return grid, start, end, walls


def bfs(grid, cell):
    q, seen = deque([cell]), {cell: 0}
    while q:
        x, y = q.popleft()
        for n in [(x + dx, y + dy) for dx, dy in DIRECTIONS]:
            if grid[(n)] == OBSTACLE:
                continue
            if n in seen:
                continue
            seen[n] = seen[(x, y)] + 1
            q.append(n)

    return seen


@timer
def find_cheats_under_n_picoseconds(lines, pico_seconds, allowed_clips):
    grid, start, end, walls = parse_input(lines)
    src = bfs(grid, start)
    dest = bfs(grid, end)
    
    seen_paths_from_start = src[end]

    cheats = []
    for ((r1, c1), n1), ((r2, c2), n2) in combinations(src.items(), 2):
        d = abs(r1 - r2) + abs(c1 - c2)
        if d <= allowed_clips and abs(n2 - n1) >= d + pico_seconds:
            cheats.append(1)
    
    # for p, v in grid.items():
    #     if v == OBSTACLE:
    #         continue
    #     x, y = p
    #     for n in [(x + dx, y + dy) for dx, dy in DIRECTIONS]:
    #         if n not in grid or grid[n] == OBSTACLE:
    #             continue
    #         print(abs(p[0] - n[0]) + abs(p[1] - n[1]))
    #         cheat = src[p] + abs(p[0] - n[0]) + abs(p[1] - n[1]) + dest[n]
    #         yield cheat <= seen_paths_from_start - pico_seconds

    return cheats

def dijkstra(starts, neighbors, cost=None):    
    pq, paths, steps = [], {}, {}
    cost = lambda c, n: 1

    for start in starts:
        heapq.heappush(pq, (start, 0))
        paths[start] = None
        steps[start] = 0

    while pq:
        current, c = heapq.heappop(pq)
        for n in neighbors(current):
            new_cost = steps[current] + cost(current, n)
            if n not in steps or new_cost < steps[n]:
                steps[n] = new_cost
                heapq.heappush(pq, (n, new_cost))
                paths[n] = current

    return paths, steps


@timer
def find_cheats_under_n_picoseconds_dijkstra(lines, pico_seconds, allowed_clips, part1 = True):
    '''
    Use dijkstra to find shortest path coordinates then reconstruct it from end to start.
    Use it to find the Manhattan distance between those cells since we can only move horizontally or vertically.
    This is slow.
    '''
    grid, start, end, walls = parse_input(lines)
    
    def find_neighbors(x, y, size):
        #cells = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        cells = [(x+dx, y+dy) for dx, dy in DIRECTIONS]
        return [(x, y) for (x, y) in cells if x >= 0 and x < size and y >= 0 and y < size]
    
    def neighbors(n):
        return [x for x in find_neighbors(*n, 1e9) if x not in walls]
    
    linked_paths, _ = dijkstra([start], neighbors)
    
    path, cheats = [], []
    while end != start:
        path.append(end)
        end = linked_paths[end]
    path.append(start)

    for i, p in enumerate(path):
        # The cheat must skip at least pico_seconds + allowed_clips steps (since cheat takes allowed_clips moves)
        for j in range(i + pico_seconds + allowed_clips, len(path)):
            dist = abs(path[j][0] - path[i][0]) + abs(path[j][1] - path[i][1])
            if (j - i) - dist < pico_seconds:
                continue

            if dist == allowed_clips and part1:
                cheats.append(1)
                
            if dist < allowed_clips+1 and not part1:
                cheats.append(1)

    return cheats


@timer 
def find_cheats_under_n_picoseconds_combo(lines, pico_seconds, allowed_clips, part1 = True):
    # Credit 4HbQ
    grid = {i+j*1j: c for i, r in enumerate(lines)
                  for j, c in enumerate(r) if c != OBSTACLE}
    start, = (p for p in grid if grid[p] == START)

    dist, queue = {start: 0}, [start]
    for pos in queue:
        
        for new in pos-1, pos+1, pos-1j, pos+1j:
            if new in grid and new not in dist:
                dist[new] = dist[pos] + 1
                queue += [new]

    cheats = []
    for (p,i), (q,j) in combinations(dist.items(), 2):
        d = abs((p-q).real) + abs((p-q).imag)
        
        if d == allowed_clips and j-i-d >= pico_seconds and part1:
            cheats.append(1)
        
        if d < allowed_clips+1 and j-i-d >= pico_seconds and not part1:
            cheats.append(1)
    
    return cheats
        
        
        

def main(args, data):
    lines = data.strip().split('\n')
    
    pico_seconds = 100
    if len(lines) == 15:
        pico_seconds = 20
    
    cheats1 = sum(find_cheats_under_n_picoseconds(lines, pico_seconds, 2))
    cheats2 = sum(find_cheats_under_n_picoseconds_dijkstra(lines, pico_seconds, 2))
    cheats3 = sum(find_cheats_under_n_picoseconds_combo(lines, pico_seconds, 2))

    assert cheats1 == cheats2 == cheats3
    
    assertions(args, cheats1, 5, 1452, 1411)
    return cheats1
    
if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

