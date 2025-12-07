'''
https://adventofcode.com/2025/day6
'''


from common.common import arg_parse, assertions, timer, transpose_matrix, OPERATOR_MAP
import operator
from functools import reduce


def read_data(data):
    lines = data.strip().split('\n')
    grid = [[int(num) if num.isnumeric() else num 
             for num in row_str.split()] for row_str in lines]
    return grid[:-1], grid[-1]

@timer
def solve_math_problems(grid, operators):
    #debug = []
    result = 0  
    for i, row in enumerate(grid):
        #debug.append(reduce(OPERATOR_MAP[operators[i]], row))
        result += reduce(OPERATOR_MAP[operators[i]], row)

    return result


def main(args, data):
    grid, operators = read_data(data)
    total = solve_math_problems(transpose_matrix(grid), operators)
    
    assertions(args, total, 4277556, 4405895212738, 4583860641327)
    return total

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

