'''
https://adventofcode.com/2024/day/13
'''



from collections import defaultdict
import re
from common.common import arg_parse, assertions, timer
import math
import z3

A_COST = 3
B_COST = 1

def parse_input(lines):
    a, b, prizes = [], [], []
    for line in lines:
        matches = re.findall(r'\d+', line)
        if 'A' in line:
            a.append(tuple(map(int, matches)))
        elif 'B' in line:
            b.append(tuple(map(int, matches)))
        elif 'Prize' in line:
            prizes.append(tuple(map(int, matches)))
            
    return a, b, prizes

@timer
def find_fewest_tokens_brute_force(a, b, prizes):
    tokens = 0
    for i, prize in enumerate(prizes):
        prize_x, prize_y = prize
        a_x, a_y = a[i]
        b_x, b_y = b[i]

        max_times = 100
        
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
            tokens += A_COST*x + y*B_COST
        
        
    return tokens

@timer
def find_fewest_tokens_z3(a, b, prizes):
    tokens = 0
    for i, prize in enumerate(prizes):
        solver = z3.Solver()
        t_a, t_b = z3.Ints("x1 x2")
        
        for j in range(2):
            a_x, b_x, prize = a[i][j], b[i][j], prizes[i][j]
            solver.add(a_x * t_a + b_x * t_b == prize)
            
        if solver.check() == z3.sat:                
            tokens += solver.model()[t_a].as_long() * A_COST + solver.model()[t_b].as_long() * B_COST
                
    return tokens

@timer
def find_fewest_tokens_z3_alt(data):
    tokens, machines = 0, data.split("\n\n")
    for game in machines:
        btn_a, btn_b, prize = game.split("\n")

        btn_a = [*map(lambda i: int(i[2:]), btn_a.split(": ")[1].split(", "))]
        btn_b = [*map(lambda i: int(i[2:]), btn_b.split(": ")[1].split(", "))]
        prize = [*map(lambda i: int(i[2:]), prize.split(": ")[1].split(", "))]

        solver = z3.Solver()
        times_a, times_b = z3.Ints("times_a times_b")
        solver.add(btn_a[0] * times_a + btn_b[0] * times_b == prize[0])
        solver.add(btn_a[1] * times_a + btn_b[1] * times_b == prize[1])
        if solver.check() == z3.sat:
            tokens += solver.model()[times_a].as_long() * A_COST + solver.model()[times_b].as_long() * B_COST

    return tokens
            


def main(args, data):
    lines = data.strip().split('\n')
    
    a, b, prizes = parse_input(lines)

    # 94x + 22x = 8400 & 34y + 67y = 5400
    tokens1 = find_fewest_tokens_brute_force(a, b, prizes)
    
    # Looks like system of equations.
    # Could use https://github.com/Z3Prover/z3 or https://github.com/sympy/sympy
    # PicoCTF - Mind Your Ps and Qs
    tokens2 = find_fewest_tokens_z3(a, b, prizes)
    
    assert tokens1 == tokens2
    
    assertions(args, tokens1, 480, 25629, 38839)

    return tokens1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

