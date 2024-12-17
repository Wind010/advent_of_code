'''
https://adventofcode.com/
'''



import re
from common.common import arg_parse, assertions, timer



def parse_input(lines):
    registers, program = lines.split('\n\n')
    registers = [*map(int, re.findall(r'\d+', registers))]
    program = [*map(int, re.findall(r'\d+', program))]
    
    return registers, program
        


@timer
def run_instructions(lines):
    registers, program = parse_input(lines)
    A, B, C = registers
    ptr, outputs = 0, []

    combo_operand = {0: 0, 1: 1, 2: 2, 3: 3, 4: lambda: A, 5: lambda: B, 6: lambda: C}

    while ptr < len(program):
        opcode, operand = program[ptr], program[ptr + 1]
        value = combo_operand.get(operand, lambda: operand)() if operand > 3 else operand

        match opcode:
            case 0: A = A // 2 ** value       # adv
            case 1: B ^= operand           # bxl
            case 2: B = value % 8          # bst
            case 3:                        # jnz
                if A != 0: 
                    ptr = operand
                    continue
            case 4: B ^= C                  # bxc
            case 5: outputs.append(value % 8)  # out
            case 6: B = A // (2 ** value)   # bdv
            case 7: C = A // (2 ** value)   # cdv

        ptr += 2

    return ','.join(map(str, outputs))


@timer
def run_instructions2(lines):
    registers, program = parse_input(lines)
    
    A, B, C = registers
    ptr, outputs = 0, []

    def combo_operand(value):
        match value:
            case 0 | 1 | 2 | 3:
                return value
            case 4:
                return A
            case 5:
                return B
            case 6:
                return C

    while ptr < len(program):
        opcode, operand = program[ptr], program[ptr + 1]
        
        match opcode:
            case 0:  # adv
                A //= 2 ** combo_operand(operand)
            case 1:  # bxl
                B = B ^ operand
            case 2:  # bst
                B = combo_operand(operand) % 8
            case 3:  # jnz
                if A != 0:
                    ptr = operand
                    continue  # skip the pointer increment
            case 4:  # bxc
                B = B ^ C
            case 5:  # out
                outputs.append(combo_operand(operand) % 8)
            case 6:  # bdv
                B = A // (2 ** combo_operand(operand))
            case 7:  # cdv
                C = A // (2 ** combo_operand(operand))

        ptr += 2

    return ','.join(map(str, outputs))




def main(args, data):
    lines = data.strip()
    
    output1 = run_instructions(lines)
    output2 = run_instructions2(lines)
    
    assert output1 == output2

    assertions(args, output1, "4,6,3,5,6,3,5,2,1,0", "1,2,3,1,3,2,5,3,1", "1,3,7,4,6,4,2,3,5")
    return output1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

