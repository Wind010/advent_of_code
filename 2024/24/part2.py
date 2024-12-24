'''
https://adventofcode.com/2024/day/24
'''



import re
from common.common import arg_parse, assertions, timer
from part1 import parse_input, process_gates


@timer
def find_swapped_wires_graphviz(data):
    '''
    '''
    pass


@timer
def find_swapped_wires_ripple_carry_adder(data):
    '''
    https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder
    '''
    bits, gates = parse_input(data)

    swapped, carry = [], None
    def do_operation(ta, tb, top):
        for a, b, op, res in gates:
            if ((a, b) == (ta, tb) or (a, b) == (tb, ta)) and op == top:
                return res
        return None
    
    Z = 'z'
    z_count = sum(1 for a, b, op, res in gates if res.startswith(Z))
    for i in range(z_count - 1):
        sum_1 = do_operation(f"x{i:02d}", f"y{i:02d}", 'XOR')
        carry_1 = do_operation(f"x{i:02d}", f"y{i:02d}", 'AND')

        if carry is not None:
            carry_2 = do_operation(carry, sum_1, 'AND')
            if carry_2 is None:
                carry_1, sum_1 = sum_1, carry_1
                swapped.extend([sum_1, carry_1])
                carry_2 = do_operation(carry, sum_1, 'AND')

            sum_2 = do_operation(carry, sum_1, 'XOR')
            if sum_1 is not None and sum_1.startswith(Z):
                sum_1, sum_2 = sum_2, sum_1
                swapped.extend([sum_1, sum_2])

            if carry_1 is not None and carry_1.startswith(Z):
                carry_1, sum_2 = sum_2, carry_1
                swapped.extend([carry_1, sum_2])

            if carry_2 is not None and carry_2.startswith(Z):
                carry_2, sum_2 = sum_2, carry_2
                swapped.extend([carry_2, sum_2])

            new_carry = do_operation(carry_2, carry_1, 'OR')
        else:
            new_carry = None

        if new_carry is not None and new_carry.startswith(Z) and new_carry != f"z{z_count-1:02d}":
            new_carry, sum_2 = sum_2, new_carry
            swapped.extend([new_carry, sum_2])

        if carry is not None:
            carry = new_carry
        else:
            carry = carry_1

    return ','.join(sorted(swapped))


def main(args, data):
    lines = data.strip().split('\n')
    
    total = find_swapped_wires_ripple_carry_adder(lines)

    assertions(args, total, "", "", "fgt,fpq,nqk,pcp,srn,z07,z24,z32", "fkb,nnr,rdn,rqf,rrn,z16,z31,z37")
    return total
    


if __name__ == "__main__":
    #args = arg_parse(__file__, 'input1.txt', main)
    #args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input4.txt', main)
