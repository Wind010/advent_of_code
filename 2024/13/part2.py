'''
https://adventofcode.com/2024/day/13
'''


import re
from common.common import arg_parse, assertions, timer
import math
import z3
from part1 import parse_input, A_COST, B_COST
import numpy as np


CONVERSION_FACTOR = 10000000000000

@timer
def find_fewest_tokens_brute_force(a, b, prizes):
    tokens = 0
    for i, prize in enumerate(prizes):
        prize_x, prize_y = prize
        a_x, a_y = a[i]
        b_x, b_y = b[i]

        max_times = CONVERSION_FACTOR * 2
        
        sol_x, sol_y = [], [] 
        for x in range(max_times):
            for y in range(max_times):
                if a_x * x + b_x * y == prize_x:
                    sol_x.append((x, y))
 
        for x in range(max_times):
            for y in range(max_times):
                if a_y * x + b_y * y == prize_y:
                    sol_y.append((x, y))
                    break
    
        #print(sol_x, sol_y)
        #print(set(sol_x).intersection(sol_y))
        
        intersect = list(set(sol_x).intersection(sol_y))
        if intersect:
            x, y = intersect[0]
            tokens += A_COST*x + B_COST*y
        
        
    return tokens

@timer
def find_fewest_tokens_z3(a, b, prizes):
    tokens = 0
    for i, prize in enumerate(prizes):
        solver = z3.Solver()
        t_a, t_b = z3.Ints("x1 x2")
        
        for j in range(2):
            a_x, b_x, prize = a[i][j], b[i][j], prizes[i][j]
            prize += CONVERSION_FACTOR # Same code as part1 just updated factor.
            solver.add(a_x * t_a + b_x * t_b == prize)
            
        if solver.check() == z3.sat:                
            tokens += solver.model()[t_a].as_long() * A_COST + solver.model()[t_b].as_long() * B_COST
                
    return tokens


@timer
def find_fewest_tokens_linear_algebra_cramer(a, b, prize):
    prize = tuple(p + CONVERSION_FACTOR for p in prize)
    # Use Cramer's rule to solve the system of equations.
    #ax + bx = px
    #by + by = py
    # det = ax*by - bx*by
    # det=a[0]⋅b[1]−a[1]⋅b[0]
    # x = det_x/det and y = det_y/
    a_presses = (b[0]* prize[1] - b[1]*prize[0])/ (b[0]*a[1] - b[1]*a[0])
    b_presses = (a[0]* prize[1] - a[1]*prize[0])/ (a[0]*b[1] - a[1]*b[0])

    if a_presses//1 == a_presses and b_presses//1 == b_presses:
        return A_COST * int(a_presses) + B_COST * int(b_presses)

    return 0

@timer
def find_fewest_tokens_linear_algebra_numpy(a, b, prize):
    ax, ay, bx, by, px, py = a[0], a[1], b[0], b[1], prize[0], prize[1]
    button_matrix = np.array([[ax, bx], [ay, by]])
    prize_matrix = np.array([px, py]) + CONVERSION_FACTOR
    a, b = map(round, np.linalg.solve(button_matrix, prize_matrix))
    return a * A_COST + b * B_COST if [a*ax + b*bx, a*ay + b*by] == [*prize_matrix] else 0


@timer
def find_fewest_tokens_linear_algebra_divmod(a, b, prize):
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    px, py = tuple(p + CONVERSION_FACTOR for p in prize)
    a, ra = divmod(py * bx - px * by, ay * bx - ax * by)
    b, rb = divmod(py * ax - px * ay, by * ax - bx * ay)
    return 3 * a + b if ra == 0 == rb else 0



def main(args, data):
    lines = data.strip().split('\n')
    
    a, b, prizes = parse_input(lines)

    # Could have tried binary search brute force?
    # https://book.jorianwoltjer.com/cryptography/custom-ciphers/z3-solver
    # https://www.youtube.com/watch?v=7WvXmoyfiTE
    
    #tokens1 = find_fewest_tokens_brute_force(a, b, prizes)
    tokens2 = find_fewest_tokens_z3(a, b, prizes)
    tokens3 = sum(find_fewest_tokens_linear_algebra_cramer(a[i], b[i], prize) for i, prize in enumerate(prizes))
    tokens4 = sum(find_fewest_tokens_linear_algebra_numpy(a[i], b[i], prize) for i, prize in enumerate(prizes))
    tokens5 = sum(find_fewest_tokens_linear_algebra_divmod(a[i], b[i], prize) for i, prize in enumerate(prizes))

    assert tokens2 == tokens3 == tokens4 == tokens5
    
    assertions(args, tokens4, 0, 107487112929999, 75200131617108)

    return tokens2
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input4.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

