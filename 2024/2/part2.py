'''
--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
'''



from common.common import arg_parse, timer
from part1 import is_safe_reactor

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

def check_reactors_cleaner(levels, limit=3):
    return [
        is_safe_reactor(numbers, limit) or
        any(is_safe_reactor(numbers[:i] + numbers[i + 1:], limit) for i in range(len(numbers)))
        for level in levels
        for numbers in [list(map(int, level.split()))]
    ]

def check_reactors_cleaner_with_safe_reactors_only(levels, limit=3):
    return [
        any(is_safe_reactor(numbers[:i] + numbers[i + 1:], limit) for i in range(len(numbers) + 1))
        for level in levels
        for numbers in [list(map(int, level.split()))]
    ]
    
    
def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.strip().split('\n')

    safe_reactors = check_reactors_cleaner(lines)
    safe_count = safe_reactors.count(True)
    #print(safe_reactors)
    print(safe_count)
    
    if 'input1.txt' in file_path: assert safe_count == 4
    if 'input2.txt' in file_path: assert safe_count == 386

    return safe_reactors
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

