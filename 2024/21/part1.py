'''
https://adventofcode.com/2024/day/21
'''


import re
from common.common import arg_parse, assertions, timer

'''
789
456
123
*0A
'''


A = 'A'
UP = '^'
DOWN = 'v'
LEFT = '>'
RIGHT = '<'

#NUMBER_PAD = {(0, 0): '7', (1, 0): '8', (2, 0): '9', (0, 1): '4', (1, 1): '5', (2, 1): '6', (0, 2): '1', (1, 2): '2', (2, 2): '3', (1, 3): '0', (2, 3): A}
NUMBER_PAD = {(0, 0): '7', (0, 1): '8', (0, 2): '9', (1, 0): '4', (1, 1): '5', (1, 2): '6', (2, 0): '1', (2, 1): '2', (2, 2): '3', (3, 1): '0', (3, 2): A}
DIRECTION_PAD = {(0, 1): UP, (0, 2): A, (1, 0): LEFT, (1, 1): DOWN, (1, 2): RIGHT}


@timer
def enter_codes(lines):
    num_pad, dir_pad = NUMBER_PAD, DIRECTION_PAD
    # Merge operator to update with gaps.
    num_pad |= ({v:k for k,v in NUMBER_PAD.items()})
    dir_pad |= ({v:k for k,v in DIRECTION_PAD.items()})
    
    #print(num_pad)
    #print(dir_pad)
        

    my_commands = [gsc(line, num_pad) for line in lines]
    r1_commands = [gsc(cmd, dir_pad) for cmd in my_commands]
    r2_commands = [gsc(cmd, dir_pad) for cmd in r1_commands]
    return sum(len(cmd)*int(line[:-1]) for cmd, line in zip(r2_commands, lines))


def step(src, dest, pad):
    si, sj = pad[src]
    ti, tj = pad[dest]
    
    di, dj = ti - si, tj - sj
    
    vertical = DOWN * di + UP * -di
    horizontal = RIGHT * dj + LEFT * -dj
    
    #print(vertical)
    #print(horizontal)
    
    if dj > 0 and (ti, sj) in pad:
        return vertical + horizontal + A
    if (si, tj) in pad:
        return horizontal + vertical + A
    if (ti, sj) in pad:
        return vertical + horizontal + A

def get_shortest_commands(path, pad):
    commands = []
    start = A
    for end in path:
        commands.append(step(start, end, pad))
        start = end
    return commands

def gsc(path, pad):
    return ''.join(get_shortest_commands(path, pad))


def main(args, data):
    lines = data.strip().split('\n')
    
    # list(map(int, sum([re.findall('\d+', m) for m in lines], [])))
    code  = [code for code in lines]
    numeric  = [int(code[:-1]) for code in lines]
    
    complexities = enter_codes(lines)
    
    assertions(args, complexities, 126384, 176650, 152942)
    return complexities
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)


