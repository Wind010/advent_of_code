'''
https://adventofcode.com/2024/day/2
'''


from common.common import arg_parse, timer, assertions


def check_reactors(lines):
    res = []
    for line in lines:
        level = list(map(int, line.split()))
        res.append(is_safe_reactor(level, 3))
    return res


def is_safe_reactor(level, limit=3):
    up, down = True, True # Ensure trend/monotonicity
    for prev, cur in zip(level, level[1::]):
        if cur > prev:
            down = False
        elif cur < prev:
            up = False

        diff = abs(prev - cur)
        if diff > limit or diff == 0:
            return False
        
    return up or down

@timer
def is_safe_reactor2(levels, limit=3):
    diff = [a - b for a, b in zip(levels, levels[1:])]
    is_in_range = all(0 < abs(i) <= limit for i in diff)
    is_monotonic = all(i > 0 for i in diff) or all(i < 0 for i in diff) # Ensure increasing or decreasing.
    if is_monotonic and is_in_range:
        return True
    return False



def main(args, data):
    lines = data.strip().split('\n')

    res = check_reactors(lines).count(True)

    assertions(args, res, 2, 321)

    return res
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

