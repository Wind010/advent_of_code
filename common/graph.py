from queue import PriorityQueue
import heapq
import numpy as np


def neighbors4(i, j, max_i, max_j=None):
    if isinstance(max_i, list):
        max_j = len(max_i[0])
        max_i = len(max_i)

    if not max_j:
        max_j = max_i

    cells = [
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1),
    ]

    return [(x, y) for (x, y) in cells if x >= 0 and x < max_i and y >= 0 and y < max_j]


def neighbors8(i, j, max_i, max_j=None):
    if isinstance(max_i, list) or isinstance(max_i, tuple):
        max_j = len(max_i[0])
        max_i = len(max_i)

    if not max_j:
        max_j = max_i

    cells = [
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1),
        (i - 1, j - 1),
        (i - 1, j + 1),
        (i + 1, j - 1),
        (i + 1, j + 1),
    ]

    return [(x, y) for (x, y) in cells if x >= 0 and x < max_i and y >= 0 and y < max_j]


def neighbors6(i, j, k, max_i, max_j=None, max_k=None, min=0):
    if (
        isinstance(max_i, list)
        and isinstance(max_i[0], list)
        and isinstance(max_i[0][0], list)
    ):
        max_i = len(max_i)
        max_j = len(max_i[0])
        max_k = len(max_i[0][0])

    if not max_j:
        max_j = max_i
    if not max_k:
        max_k = max_i

    cells = [
        (i - 1, j, k),
        (i + 1, j, k),
        (i, j - 1, k),
        (i, j + 1, k),
        (i, j, k - 1),
        (i, j, k + 1),
    ]

    return [
        (x, y, z)
        for (x, y, z) in cells
        if x >= -10 and x < max_i and y >= -10 and y < max_j and z >= -10 and z < max_k
    ]


def dijkstra(starts, neighbors, cost=None):
    if not isinstance(starts, list):
        starts = [starts]
    if cost is None:
        cost = lambda c, n: 1

    front = PriorityQueue()
    came_from, cost_so_far = {}, {}

    for start in starts:
        front.put(start, 0)
        came_from[start] = None
        cost_so_far[start] = 0

    while not front.empty():
        current = front.get()

        for next in neighbors(current):
            new_cost = cost_so_far[current] + cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                front.put(next, new_cost)
                came_from[next] = current

    return came_from, cost_so_far


def a_star(starts, goal, neighbors, cost=None, heuristic=None):
    if not isinstance(starts, list):
        starts = [starts]
    if heuristic is None:
        heuristic = lambda a, b: sum(abs(x - y) for x, y in zip(a, b))
    if cost is None:
        cost = lambda c, n: 1

    front = PriorityQueue()
    came_from, cost_so_far = {}, {}

    for start in starts:
        front.put(start, 0)
        came_from[start] = None
        cost_so_far[start] = 0

    while not front.empty():
        current = front.get()

        if current == goal:
            break

        for n in neighbors(current):
            new_cost = cost_so_far[current] + cost(current, n)
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                priority = new_cost + heuristic(n, goal)
                front.put(n, priority)
                came_from[n] = current

    return came_from, cost_so_far