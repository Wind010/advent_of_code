'''
https://adventofcode.com/
'''


import re
from common.common import arg_parse, assertions, timer
from part1 import parse_input, run_instructions


@timer
def find_reoccurance(lines):
    '''
    Ouroboros 
    '''
    registers, program = parse_input(lines)
    
    # Try to start off as close as possible.
    THREE_BIT_RANGE = 7  # 0-7
    A = sum(THREE_BIT_RANGE * 8**i for i in range(len(program) - 1)) + 1  # Get the sum of all 3-bit numbers of base-8.
    while True:
        #print(A)
        result = [*map(int, run_instructions([A, 0, 0], program).split(','))]

        if result == program:
            return A
        
        # oct(117440)
        # 117440 converts to 0o345300 in base-8.  So we increment accordingly by base-8 steps.
        # We optimize by decrementing in base-8 from the last last result output.
        # Adjust A based on the first mismatch, starting from the least significant bit/tail
        for i in range(len(result) - 1, -1, -1):
            if result[i] != program[i]:
                A += 8**i
                break
 
@timer
def find_reoccurance2(lines):
    '''
    Ouroboros 
    '''
    registers, program = parse_input(lines)
    A = (8**(len(program) - 1) - 1) + 1  
    while True:
        result = [*map(int, run_instructions([A, 0, 0], program).split(','))]

        if result == program:
            return A

        for i, (r, p) in reversed(list(enumerate(zip(result, program)))):
            if r != p:
                A += 8**i
                break
 

 
def main(args, data):
    lines = data.strip()
    
    min_a_value1 = find_reoccurance(lines)
    min_a_value2 = find_reoccurance2(lines)
    
    assert min_a_value1 == min_a_value2

    assertions(args, min_a_value1, 1, 105706277661082, 202367025818154, 117440)
    return min_a_value1



if __name__ == "__main__":
    args = arg_parse(__file__, 'input4.txt', main)
    #args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

