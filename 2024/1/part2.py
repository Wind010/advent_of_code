'''
--- Part Two ---
https://adventofcode.com/2024/day/1
'''

from common.common import arg_parse, assertions


def main(args, data):
    lines = data.strip().split('\n')
    
    col1 = [int(line.split()[0]) for line in lines]
    col2 = [int(line.split()[1]) for line in lines]
    
    score = sum([n * col2.count(n)for n in col1])

    assertions(args, score, 31, 24643097)

    return score
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
