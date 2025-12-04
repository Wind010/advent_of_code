'''
https://adventofcode.com/2024/day/21
'''


import re
from common.common import arg_parse, assertions, timer
from part1 import NUMBER_PAD, DIRECTION_PAD, step, get_shortest_commands, gsc
from typing import Counter


@timer
def enter_codes(lines, robots):
    num_pad, dir_pad = NUMBER_PAD, DIRECTION_PAD
    num_pad |= ({v:k for k,v in NUMBER_PAD.items()})
    dir_pad |= ({v:k for k,v in DIRECTION_PAD.items()})

    def num_commands(route):
        return sum(len(k)*v for k,v in route.items())

    my_commands = [gsc(line, num_pad) for line in lines]

    robot_cmd = [Counter([route]) for route in my_commands]
    for _ in range(robots):
        new_routes = []
        for cmd_counter in robot_cmd:
            new_cmds = Counter()
            for sub_route, qty in cmd_counter.items():
                new_counts = Counter(get_shortest_commands(sub_route, dir_pad))
                for k in new_counts:
                    new_counts[k] *= qty
                new_cmds.update(new_counts)
            new_routes.append(new_cmds)
        robot_cmd = new_routes

    return sum(num_commands(cmd)*int(line[:-1]) for cmd, line in zip(robot_cmd, lines))


def main(args, data):
    lines = data.strip().split('\n')
    
    complexities = enter_codes(lines, 25)
    
    assertions(args, complexities, 154115708116294, 217698355426872, 189235298434780)
    return complexities
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)


