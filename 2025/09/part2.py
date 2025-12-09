'''
https://adventofcode.com/2025/day9

'''


# Looks like flood fill problem?  With so many points, it might take awhile.
# Either that or calcualte all rectangles and check the largest one that fits in that rectangle?


from part1 import parse_input
from common.common import arg_parse, assertions, timer



def main(args, data):
    coords = parse_input(data)
    area = 0
    assertions(args, area, 24, 1, 1)
    return area
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

