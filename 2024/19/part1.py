'''
https://adventofcode.com/2024/day/19
'''



import re
from common.common import arg_parse, assertions, timer
from collections import defaultdict
from functools import cache


@timer
def find_possible_designs_memo1(designs, patterns):
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
def find_possible_designs_memo2(designs, patterns):

    @cache
    def match_design(design):
        if not design:
            return 1
        total = 0
        for pat in patterns.get(design[0],[]):
            if design.startswith(pat):
                total += match_design(design.removeprefix(pat))
        return total

    return sum(match_design(d) > 0 for d in designs)


@timer
def find_possible_designs_memo3(designs, patterns):
    
    @cache
    def matches(design):
        if not design:
            return 1
        #print([(design, p, matches(design[len(p):])) for p in patterns if design.startswith(p)])
        return sum( matches(design[len(p):]) for p in patterns if design.startswith(p) )

    return sum(matches(d) > 0 for d in designs)



@timer
def find_possible_designs_memo4(data):
    # Credit 4HbQ
    P, _, *D = data.split('\n')

    @cache
    def count(d):
        return d == '' or sum(count(d.removeprefix(p))
            for p in P.split(', ') if d.startswith(p))

    for _type in bool, int:
        return sum(map(_type, map(count, D)))

        

def main(args, data):
    lines = data.strip().split('\n\n')
    
    patterns, designs = lines[0].split(', '), lines[1].split('\n')
    dict_patterns = {k: [pat for pat in patterns if pat.startswith(k)]
                                                 for k in set(p[0] for p in patterns)}
    
    possible_designs1 = find_possible_designs_memo1(designs, dict_patterns)
    possible_designs2 = find_possible_designs_memo2(designs, dict_patterns)
    possible_designs3 = find_possible_designs_memo3(designs, patterns)
    possible_designs4 = find_possible_designs_memo4(data)
    assert possible_designs1 == possible_designs2 == possible_designs3 == possible_designs4
    
    assertions(args, possible_designs1, 6, 313, 350)
    return possible_designs1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    #args = arg_parse(__file__, 'input2.txt', main)
    #args = arg_parse(__file__, 'input3.txt', main)

