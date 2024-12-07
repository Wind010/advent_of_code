'''
https://adventofcode.com/2024/day/7
'''


import re
from functools import reduce
from itertools import product
import operator
from common.common import arg_parse, assertions, timer
from multiprocessing import Pool, cpu_count


def evaluate_combination(n, operations):
    result = n[0]
    for i, op in enumerate(operations):
        if op == operator.concat:
            result = op(str(result), str(n[i + 1]))
            result = int(result)
        else:
            result = op(result, n[i + 1])
    return result


@timer
def find_valid_calibrations(lines):
    valid_results = []
    for line in lines:
        res = process_line(line)
        if res:
            valid_results.append(res)
    return valid_results


def process_line(line):
    numbers = list(map(int, re.findall(r'\d+', line)))
    result, constants = numbers[0], numbers[1:]
    #print(result, constants)

    operations = [operator.add, operator.mul, operator.concat]
    operation_combinations = product(operations, repeat=len(constants) - 1)

    for ops in operation_combinations:
        res = evaluate_combination(constants, ops)
        if res == result:
            return result
    return None


@timer
def find_valid_calibrations_multiprocess(lines):
    '''
    Cuts time in ~1/6th
    '''
    with Pool(processes=cpu_count() // 2) as pool:
        results = pool.map(process_line, lines)
    valid_results = [res for res in results if res is not None]
    return valid_results


        
def main(args, data):
    lines = data.strip().split('\n')

    #valid_calibrations = find_valid_calibrations(lines)

    valid_calibrations = find_valid_calibrations_multiprocess(lines)
    total = sum(valid_calibrations)
    
    assertions(args, total, 11387, 124060392153684) 

    return total


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    #args = arg_parse(__file__, 'input3.txt', main)

