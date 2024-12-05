'''
https://adventofcode.com/2024/day/5
'''



import re
from common.common import arg_parse, timer, assertions
from collections import defaultdict


def parse_edges(section):
    rules = defaultdict(set)
    for line in section.split('\n'):
        for match in re.findall(r'(\d{2})\|(\d{2})', line):
            src, dest = match
            rules[src].add(dest)
    return rules


@timer
def find_valid_middle_pages_original(rules, pages):
    res = []
    skip = False
    for line in pages:
        for i, page in enumerate(line):
            for r in rules[page]:
                if r in line and line.index(r) < i:
                    skip = True
                    break
        
        if not skip:
            #print(line)
            res.append(int(line[len(line)//2]))
            skip = False
        
    return res


@timer
def find_valid_middle_pages_index_map(rules, pages):
    res = []
    for line in pages:
        # Create a dictionary to store the first occurrence index of each element in line
        index_map = {element: idx for idx, element in enumerate(line)}
        
        skip = False
        for i, page in enumerate(line):
            if skip:
                break
            for r in rules.get(page, []):
                if r in index_map and index_map[r] < i:
                    skip = True
                    break
        
        if not skip:
            #print(line)
            res.append(int(line[len(line) // 2]))
    
    return res

@timer
def find_valid_middle_pages_any(rules, pages):
    res = []
    for line in pages:
        index_map = {element: idx for idx, element in enumerate(line)}
        
        if not any(
            any(r in index_map and index_map[r] < i for r in rules.get(page, []))
            for i, page in enumerate(line)
        ):
            res.append(int(line[len(line) // 2]))
    
    return res



def main(args, data):
    sections = data.strip().split('\n\n')

    #rules = [match for line in sections[0].split('\n') for match in re.findall(r'(\d{2})\|(\d{2})', line)]
    #rules = {match[0]: match[1] for line in sections[0].split('\n') for match in re.findall(r'(\d{2})\|(\d{2})', line)}
    
    edges = parse_edges(sections[0])
    pages = [line.split(',') for line in sections[1].split('\n')]

    total1 = sum(find_valid_middle_pages_original(edges, pages))
    total2 = sum(find_valid_middle_pages_any(edges, pages))
    total3 = sum(find_valid_middle_pages_any(edges, pages))
    
    assert total1 == total2 == total3

    assertions(args, total1, 143, 4957)

    return total1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)


