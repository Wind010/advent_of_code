'''
--- Day 5: Print Queue ---
Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.

The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual pages won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the pages are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying which pages are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the right order:

75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.
Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

The second and third pages are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered pages, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered pages are:

75,47,61,53,29
97,61,53,29,13
75,29,13
These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

Determine which pages are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered pages?
'''



import re
from common.common import arg_parse, timer
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



def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    sections = data.strip().split('\n\n')

    #rules = [match for line in sections[0].split('\n') for match in re.findall(r'(\d{2})\|(\d{2})', line)]
    #rules = {match[0]: match[1] for line in sections[0].split('\n') for match in re.findall(r'(\d{2})\|(\d{2})', line)}
    
    edges = parse_edges(sections[0])
    pages = [line.split(',') for line in sections[1].split('\n')]

    total1 = sum(find_valid_middle_pages_original(edges, pages))
    total2 = sum(find_valid_middle_pages_any(edges, pages))
    total3 = sum(find_valid_middle_pages_any(edges, pages))
    
    assert total1 == total2 == total3
    
    print(total1)

    if 'input1.txt' in file_path: assert total1 == 143
    if 'input2.txt' in file_path: assert total1 == 4957


    return total1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

