'''
https://adventofcode.com/2024/day/2
'''


from common.common import arg_parse, timer, assertions
from part1 import is_safe_reactor


@timer
def check_reactors(levels):
    res = []
    for level in levels:
        levels = list(map(int, level.split()))
        is_safe = is_safe_reactor(levels)

        if is_safe:
            res.append(is_safe)
        else:
            safe_found = False
            for i in range(len(levels)):
                bad_levels = levels[:i] + levels[i + 1::]
                is_safe = is_safe_reactor(bad_levels)
                if is_safe:
                    res.append(is_safe)
                    safe_found = True
                    break
            if not safe_found:
                res.append(False)
    
    return res

@timer
def check_reactors_cleaner(levels, limit=3):
    return [
        is_safe_reactor(numbers, limit) or
        any(is_safe_reactor(numbers[:i] + numbers[i + 1:], limit) for i in range(len(numbers)))
        for level in levels
        for numbers in [list(map(int, level.split()))]
    ]


@timer
def check_reactors_cleaner_with_safe_reactors_only(levels, limit=3):
    return [
        any(is_safe_reactor(numbers[:i] + numbers[i + 1:], limit) for i in range(len(numbers) + 1))
        for level in levels
        for numbers in [list(map(int, level.split()))]
    ]
    
    
def main(args, data):
    lines = data.strip().split('\n')

    safe_reactors = check_reactors(lines)
    safe_count = safe_reactors.count(True)
    #print(safe_reactors)
    print(safe_count)
    
    assertions(args, safe_count, 4, 386)

    return safe_reactors
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

