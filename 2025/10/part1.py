'''
https://adventofcode.com/2025/day10
'''


import re
from common.common import arg_parse, assertions, timer
from collections import deque

# Maybe there is a quicker or elegant way with some binary tricks?  
# Could brute force and compare each set of presses to the current lights (translated to . and #) and compare to expected lights. 
# Finding the min means by number of presses using BFS examining 1 presses to N presses.

def parse_input(data):
    # Times like these I wish I had regex skills
    brackets, paren, curly = [], [], []
    for line in data.strip().splitlines():
        #print(line)
        b, p, c = [], [], []
        i = 0
        while i < len(line):
        
            if line[i] == '[':
                end = line.find(']', i)
                if end != -1:
                    b = [*line[i+1:end]]
                    i = end + 1
            elif line[i] == '(':
                end = line.find(')', i)
                if end != -1:
                    p.append(line[i+1:end])
                    i = end + 1
            elif line[i] == '{':
                end = line.find('}', i)
                if end != -1:
                    c.append(line[i+1:end])
                    i = end + 1
            else:
                i += 1
        
        # Just convert to indexes of where lights are on for easy comparison.
        b = tuple(i for i, t in enumerate(b) if t == '#')
        p = [tuple(map(int, x.split(','))) for x in p]
        c = [tuple(map(int, x.split(','))) for x in c]
        
        brackets.append(b)
        paren.append(p)
        curly.append(c)
        
    return brackets, paren, curly

def parse_input2(data):
    res = []
    lines = data.strip().splitlines()
    for line in lines:
        brackets, *paren, curly = line.split()
        brackets = [x == "#" for x in brackets[1:-1]]
        parens = [tuple(map(int, p[1:-1].split(","))) for p in paren]
        curly = list(map(int, curly[1:-1].split(",")))
        res.append((brackets, parens, curly))
    return res
    
    
def find_min_presses_bfs(target_lights, presses):
    target_lights, presses = set(target_lights), list(map(set, presses))
    q = deque()
    q.append((set(), 0))
    seen = set()
    steps = 0
    while q:
        curr, steps = q.popleft()
        if curr == target_lights:
            return steps
        for p in presses:
            diff_set = curr.symmetric_difference(p) # XOR 
            f = frozenset(diff_set) # Can't hash the set, has to be frozenset.
            if f in seen:
                continue
            seen.add(f)
            q.append((diff_set, steps + 1))



def main(args, data):
    lights, presses, joltage = parse_input(data)
    #print(lights, presses, joltage)
    
    total = sum(find_min_presses_bfs(lights[i], presses[i]) for i in range(len(lights)))

    assertions(args, total, 7, 457, 449)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

