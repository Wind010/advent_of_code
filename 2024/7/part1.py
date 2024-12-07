'''
https://adventofcode.com/2024/day/7
'''


import re
from functools import reduce
from itertools import product
import operator
from common.common import arg_parse, assertions, timer


def evaluate_combination(n, operations):
    ''' Time complexity of O(n*o) '''
    result = n[0]
    for i, op in enumerate(operations):
        result = op(result, n[i + 1])
    return result

# def evaluate_combination(n, operations):
#     return reduce(lambda x, y: y[0](x, y[1]), zip(operations, n[1:]), n[0])

@timer
def find_valid_calibrations(lines):
    ''' 
    Time complexity of O(n*o*l) where n is the number of constants
    , o is operations 2 and l is number of lines.  Ignoring the regex parse.
    Could save memory by just summing as we go instead of all the results.
    '''
    valid_results = []
    for line in lines:
        numbers = list(map(int, re.findall(r'\d+', line)))
        result, constants = numbers[0], numbers[1:]
        #print(result, constants)

        operations = [operator.add, operator.mul]
        operation_combinations = list(product(operations, repeat=len(constants) - 1))

        for ops in operation_combinations:
            res = evaluate_combination(constants, ops)
            if res == result:
                valid_results.append(result)
                break
        
    return valid_results


        
def main(args, data):
    lines = data.strip().split('\n')

    valid_calibrations = find_valid_calibrations(lines)
    total = sum(valid_calibrations)
    assertions(args, total, 3749, 124060392153684) 

    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    #args = arg_parse(__file__, 'input3.txt', main)

