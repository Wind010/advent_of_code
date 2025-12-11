'''
https://adventofcode.com/2025/day10
'''

# Use PuLP or SciPy linprog to solve as integer linear programming problem.

from part1 import parse_input
from common.common import arg_parse, assertions, timer
from scipy.optimize import linprog


def find_min_presses_linear_alg(presses, joltages):
    presses, joltages = list(map(tuple, presses)), tuple(*joltages)
    costs = [1] * len(presses) # OR [1 for p in presses] 1 per button.
    #eqs[i][p] is True if press contribues to joltage[i]
    eqs = [[i in p for p in presses] for i in range(len(joltages))]
    # min(cost * x) subject to eqs * x = joltages
    
    return linprog(costs, A_eq=eqs, b_eq=joltages, integrality=1).fun


def main(args, data):
    lights, presses, joltages = parse_input(data)
    #print(lights, presses, joltage)

    total = sum(find_min_presses_linear_alg(presses[i], joltages[i]) for i in range(len(lights)))
    total = int(total) # If we cast to int within the loop we are off by 1, sometimes, due to rounding.
    
    assertions(args, total, 33, 17576, 17848)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

