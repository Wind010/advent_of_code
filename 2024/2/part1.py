'''
--- Day 2: Red-Nosed Reports ---
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?
'''


import re
from common.common import arg_parse, timer


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


def is_safe_reactor2(levels, limit=3):
    diff = [a - b for a, b in zip(levels, levels[1:])]
    is_in_range = all(0 < abs(i) <= limit for i in diff)
    is_monotonic = all(i > 0 for i in diff) or all(i < 0 for i in diff) # Ensure increasing or decreasing.
    if is_monotonic and is_in_range:
        return True
    return False



def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.strip().split('\n')

    res = check_reactors(lines).count(True)
    
    print(res)
    
    if 'input1.txt' in file_path: assert res == 2
    if 'input2.txt' in file_path: assert res == 321

    return res
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

