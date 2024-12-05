'''
See https://adventofcode.com/2024/day/1
'''


from common.common import arg_parse, assertions, timer


def main(args, data):
    lines = data.strip().split('\n')
    
    col1 = sorted(int(line.split()[0]) for line in lines)
    col2 = sorted(int(line.split()[1]) for line in lines)
    
    res = [abs(n1 - n2) for n1, n2 in zip(col1, col2)]
    
    total = sum(res)

    assertions(args, total, 11, 2769675)

    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

