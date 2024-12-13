'''
https://adventofcode.com/2024/day/13
'''


import re
from common.common import arg_parse, assertions, timer
import math
import z3
from part1 import parse_input


CONVERSION_FACTOR = 10000000000000

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
            tokens += 3*x + y
        
        
    return tokens


def find_fewest_tokens_z3(a, b, prizes):
    tokens = 0
    for i, prize in enumerate(prizes):
        solver = z3.Solver()
        t_a, t_b = z3.Ints("x1 x2")
        
        for j in range(2):
            a_x, b_x, prize = a[i][j], b[i][j], prizes[i][j]
            prize += CONVERSION_FACTOR
            solver.add(a_x * t_a + b_x * t_b == prize)
            
        if solver.check() == z3.sat:                
            tokens += solver.model()[t_a].as_long() * 3 + solver.model()[t_b].as_long()
                
    return tokens


def main(args, data):
    lines = data.strip().split('\n')
    
    a, b, prizes = parse_input(lines)

    # Could have tried binary search brute force?
    # https://book.jorianwoltjer.com/cryptography/custom-ciphers/z3-solver
    # https://www.youtube.com/watch?v=7WvXmoyfiTE
    #tokens1 = find_fewest_tokens_brute_force(a, b, prizes)
    tokens2 = find_fewest_tokens_z3(a, b, prizes)
    
    #assert tokens1 == tokens2
    
    assertions(args, tokens2, 0, 107487112929999, 75200131617108)

    return tokens2
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input4.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

