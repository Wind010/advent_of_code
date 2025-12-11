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
        b = set(i for i, t in enumerate(b) if t == '#')
        p = [set(map(int, x.split(','))) for x in p]
        c = [set(map(int, x.split(','))) for x in c]
        
        brackets.append(b)
        paren.append(p)
        curly.append(c)
        
    return brackets, paren, curly



def find_min_presses_bfs(target_lights, presses):
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

