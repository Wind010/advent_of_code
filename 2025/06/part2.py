'''
https://adventofcode.com/2025/day6
'''

from part1 import read_data



from common.common import arg_parse, assertions, timer, transpose_matrix, OPERATOR_MAP, rotate_180
import operator
from functools import reduce



def read_data(data):
    grid, operators = [], None
    for line in data.splitlines():
        if "+" in line:
            operators = line
        else:
            grid.append(line)
    return grid, operators


def extract_numbers_from_columns(grid, start_col, width):
    numbers = []
    for col in range(start_col, start_col + width):
        value = 0
        for row in grid:
            # Damn spaces
            if row[col] != " ":
                value = value * 10 + int(row[col])
        numbers.append(value)
    return numbers


def calculate_result(grid, operators):
    result = 0
    for idx, op in enumerate(operators):
        # Damn spaces
        if op != " ":
            next_idx = idx + 1
            while next_idx < len(operators) and operators[next_idx] == " ":
                next_idx += 1
            group_width = next_idx - idx
            if next_idx < len(operators):
                group_width -= 1

            numbers = extract_numbers_from_columns(grid, idx, group_width)

            result += reduce(OPERATOR_MAP[op], numbers)

            # We only have two operators, but we use helper function anyways.
            # if op == "+":
            #     result += sum(numbers)
            # elif op == "*":
            #     result += reduce(operator.mul, numbers)

    return result

 
def main(args, data):
    grid, operators = read_data(data)
    total = calculate_result(grid, operators)
    assertions(args, total, 3263827, 7450962489289, 11602774058280)
    return total

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

