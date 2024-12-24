'''
https://adventofcode.com/2024/day/24
'''



import re
from common.common import arg_parse, assertions, timer
import operator


def parse_input(lines):
    wires, gates = {}, []
    for line in lines:
        if ':' in line:
            w = line.split(':')
            wires[w[0]] = int(w[1].strip())
        elif line == '':
            continue
        else:
            g = line.split(' ')
            gates.append((g[0], g[2], g[1], g[4]))
    
    #print(gates)
    return wires, gates
        
def process_gates(data):
    wires, gates = parse_input(data)
    operators = {
        'AND': operator.__and__,
        'OR': operator.__or__,
        'XOR': operator.__xor__
        
    }
    
    d_gates = {}
    while len(d_gates) < len(gates):
        for g1, g2, op, res in gates:
            if g1 in wires and g2 in wires:
                d_gates[res] = operators[op](wires[g1], wires[g2])
            elif g1 in wires and g2 in d_gates:
                d_gates[res] = operators[op](wires[g1], d_gates[g2])
            elif g1 in d_gates and g2 in wires:
                d_gates[res] = operators[op](d_gates[g1], wires[g2])
            elif g1 in d_gates and g2 in d_gates:
                d_gates[res] = operators[op](d_gates[g1], d_gates[g2])
                
    sorted_keys = sorted([key for key in d_gates.keys() if key.startswith('z')], reverse=True)
    binary_string = ''.join(str(d_gates[key]) for key in sorted_keys)
    
    print(sorted_keys, binary_string)
    
    return int(binary_string, 2)
    
    


def main(args, data):
    lines = data.strip().split('\n')
    
    total = process_gates(lines)

    assertions(args, total, 4, 2024, 61886126253040, 53325321422566)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input4.txt', main)

