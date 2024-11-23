'''
--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.
You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.
Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.
This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.
Consider the same engine schematic again:

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
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
'''

import re

from common.common import arg_parse
from helpers import DIRECTIONS, SYMBOLS, DOT, ASTERISK, Number


def find_adjacent_numbers(x, y, numbers):
    found = []
    for number in numbers:
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) in number.pos:
                found.append(number.value)
                break
    return found


def scan_numbers_and_gears(matrix):
    rows, cols = len(matrix), len(matrix[0])
    numbers, n, number = [], '', Number()
    gears = []
    
    def flush(number, n):
        number.value = int(n)
        numbers.append(number)
        number = Number()
        n = ''
        return number, n
        
    for x in range(rows):
        for y in range(cols):
            c = matrix[x][y]
            #print(x, y, c)

            if c == ASTERISK:
                gears.append((x, y))
            
            if c.isdigit():
                number.pos.append((x, y))
                n += c
            elif n:
                number, n = flush(number, n)
            else:
                #if n: print(n, adjacent)
                n = ''
        
        # Handle that last element/cell.
        if n:
            number, n = flush(number, n)
            
    return (gears, numbers)
                
  
def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')
    
    # Find the numbers and gear positions.
    gears, numbers = scan_numbers_and_gears(lines)
    
    total_sum = 0
    for gear in gears:
        # For each gear/asterisks look in all 8 cell directions to determine if those cells overlap with numbers.
        n = find_adjacent_numbers(*gear, numbers) 
        if len(n) == 2:
            # Could be more than 2 numbers, but we break on first hit in find_adjacent_numbers.
            total_sum += n[0] * n[1]
        
    
    print(total_sum)
    if 'input1.txt' in file_path: assert total_sum == 467835 
    if 'input2.txt' in file_path: assert total_sum == 81721933 #81742523

    return total_sum

 
if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)
