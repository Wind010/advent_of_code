'''
https://adventofcode.com/2025/day3
'''

from common.common import arg_parse, assertions, timer


def find_max_joltage(bank, k):
    # Looks like a max subsequence problem
    stack = []
    to_remove = len(bank) - k
    for d in bank:
        while stack and to_remove > 0 and stack[-1] < d:
            stack.pop()
            to_remove -= 1
        stack.append(d)
        
    return int(''.join(map(str, stack[:k])))


def main(args, data):
    lines = data.strip().split('\n')
    
    total = sum(find_max_joltage(line, 12) for line in lines)
 

    assertions(args, total, 3121910778619, 169935154100102, 170147128753455)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

