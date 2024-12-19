'''
https://adventofcode.com/2024/day/19
'''



import re
from common.common import arg_parse, assertions, timer
from collections import defaultdict
from functools import cache



@timer
def find_all_possible_designs_memo1(designs, patterns):
    memo = {}
    def match_design(design):
        if design in memo:
            return memo[design]
        if not design:
            return 1
        total = 0
        for pat in patterns.get(design[0], []):
            if design.startswith(pat):
                total += match_design(design.removeprefix(pat))
        memo[design] = total
        return total

    return sum(match_design(d) > 0 for d in designs)


@timer
def find_all_possible_designs_memo2(designs, patterns):
    @cache
    def match_design(design):
        if not design:
            return 1
        total = 0
        for pat in patterns.get(design[0],[]):
            if design.startswith(pat):
                total += match_design(design.removeprefix(pat))
        return total

    return sum(match_design(d) for d in designs)

        

def main(args, data):
    lines = data.strip().split('\n\n')
    
    patterns, designs = lines[0].split(', '), lines[1].split('\n')
    
    dict_patterns = {k: [pat for pat in patterns if pat.startswith(k)]
                                                 for k in set(p[0] for p in patterns)}
    
    
    possible_designs1 = find_all_possible_designs_memo1(designs, dict_patterns)
    possible_designs1 = find_all_possible_designs_memo2(designs, dict_patterns)
    
    assert possible_designs1 == possible_designs2

    assertions(args, possible_designs1, 16, 666491493769758, 769668867512623)
    return possible_designs1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

