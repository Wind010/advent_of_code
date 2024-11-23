'''
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.
It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.
"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)
Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
'''


import re

from common.common import arg_parse
from helpers import DIRECTIONS, SYMBOLS, DOT


def is_adjacent(rows, cols, x, y, matrix):
    for dx, dy in DIRECTIONS:
        new_x, new_y = x + dx, y + dy
        if new_x < 0 or new_x >= rows:
            continue
        if new_y < 0 or new_y >= cols:
            continue
        
        neighbor = matrix[new_x][new_y]
        #print(new_x, new_y, neighbor)
        if neighbor in SYMBOLS:
            return True
    return False

                
def scan_part_numbers(matrix):
    rows, cols = len(matrix), len(matrix[0])
    numbers, n, adjacent = [], '', False
    for x in range(rows):
        for y in range(cols):
            c = matrix[x][y]
            #print(x, y, c)
 
            if c != DOT and not adjacent:
                adjacent = is_adjacent(rows, cols, x, y, matrix)

            if c.isdigit():
                n += c
            elif n and adjacent:
                numbers.append(int(n))
                n = ''
                adjacent = False
            else:
                #if n: print(n, adjacent)
                n = ''
                
        if n and adjacent:
            numbers.append(int(n))
            adjacent = False

    return numbers
                
                    
                    
def get_numbers(lines):
    numbers, n = [], ''
    for line in lines:
        for c in line:
            if c.isdigit():
                n += c
            elif n:
                numbers.append(int(n))
                n = ''
        if n:
            numbers.append(int(n))
            n = ''

    return numbers

  
def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')
    
    # Scratch:
    # flat_list = [item for sublist in list_of_lists for item in sublist]
    all_digits =  [int(c) for line in lines for c in re.findall(r'\d+', line)]
    all_digits2 = get_numbers(lines);
    all_digits3 = [int(n) for line in lines for n in ''.join(c if c.isdigit() else ' ' for c in line).split()]

    assert all_digits == all_digits2 == all_digits3


    # Actual
    parts = scan_part_numbers(lines)
    total_sum = sum(parts)
    
    print(total_sum)
    if 'input1.txt' in file_path: assert total_sum == 4361 
    if 'input2.txt' in file_path: assert total_sum == 522726 

    return total_sum
    
    

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)
