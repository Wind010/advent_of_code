'''
https://adventofcode.com/2024/day/13
'''



from collections import defaultdict
import re
from common.common import arg_parse, assertions, timer
import math
import z3

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
            tokens += 3*x + y
        
        
    return tokens



def main(args, data):
    lines = data.strip().split('\n')
    
    a, b, prizes = parse_input(lines)

    # 94x + 22x = 8400 & 34y + 67y = 5400
    tokens1 = find_fewest_tokens_brute_force(a, b, prizes)
    
    assertions(args, tokens1, 480, 25629) # 38839

    return tokens1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

