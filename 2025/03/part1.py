'''
https://adventofcode.com/2025/day3
'''

from common.common import arg_parse, assertions, timer


def find_max_joltage(banks):
    joltage = []
    for bank in banks:
        max_number = -1
        for i in range(len(bank) - 1):
            for j in range(i + 1, len(bank)):
                number = int(f"{bank[i]}{bank[j]}")
                if number > max_number:
                    max_number = number

        joltage.append(max_number)
    return joltage
            


def main(args, data):
    lines = data.strip().split('\n')
    total = sum(find_max_joltage(lines))
    assertions(args, total, 357, 17142, 17092)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)


