'''
--- Part Two ---
While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

75,97,47,61,53 becomes 97,75,47,61,53.
61,13,29 becomes 61,29,13.
97,13,75,29,47 becomes 97,75,47,29,13.
After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?
'''


import re
from common.common import arg_parse, timer
from collections import defaultdict, deque


def parse_edges(section):
    # predecessors[i] is the set of pages that precede i.
    # successors[i] is the set of pages succeed i.
    predecessors, successors = defaultdict(set),  defaultdict(set)
    
    for line in section.split('\n'):
        for match in re.findall(r'(\d{2})\|(\d{2})', line):
            src, dest = map(int, match)
            predecessors[dest].add(src)
            successors[src].add(dest)
    return predecessors, successors


def is_valid_order(pages, predecessors):
    for i, page_x in enumerate(pages):
        for j, page_y in enumerate(pages):
            if i < j and page_y in predecessors[page_x]:
                return False
    return True


def is_valid_order_cleaner(pages, predecessors):
    '''Shorter, but harder to read'''
    return not any(page_y in predecessors[page_x] for i, page_x in enumerate(pages)
                   for j, page_y in enumerate(pages) if i < j)


def topological_sort(pages, predecessors, successors):
    sorted_pages = []
    
    #Calculate the in-degree of each page, which is the number of incoming edges 
    # (predecessors) for each page, considering only within pages.
    in_degree = {page: len(predecessors[page] & set(pages)) for page in pages}
    
    # Initialize the queue with pages that have no incoming edges in the subset
    queue = deque(page for page in pages if in_degree[page] == 0)

    while queue:
        current_page = queue.popleft()
        sorted_pages.append(current_page)
        for next_page in successors[current_page]:
            if next_page in in_degree:
                in_degree[next_page] -= 1
                if in_degree[next_page] == 0:
                    queue.append(next_page)
    
    return sorted_pages


@timer
def find_middle_pages_after_reorder(edges_section, pages):
    predecessors, successors = parse_edges(edges_section)
    res = []
    for line in pages:
        assert len(line) % 2 == 1, "Pages length must be odd" # Safety
        
        if is_valid_order_cleaner(line, predecessors):
            # Would have worked for part 1 here.
            #middle_element = line[len(line) // 2]
            #print(line)
            continue
        else:
            # Perform topological sort on the subset of pages in line of pages.
            sorted_pages = topological_sort(line, predecessors, successors)
            middle_element = sorted_pages[len(sorted_pages) // 2]
            res.append(middle_element)
        
    return res


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    sections = data.strip().split('\n\n')

    pages = [list(map(int, line.split(','))) for line in sections[1].split('\n')]
    
    total = sum(find_middle_pages_after_reorder(sections[0], pages))
    print(total)

    if 'input1.txt' in file_path: assert total == 123
    if 'input2.txt' in file_path: assert total == 6938


    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

