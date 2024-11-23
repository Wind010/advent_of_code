# https://adventofcode.com/2023/day/1

'''
--- Day 1: Trebuchet?! ---
--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
'''

# python 1.py /path/to/your/input2.txt

import os
import re

from common.common import arg_parse


def group_pairs(str_num_arr):
    pairs = []
    for nums in str_num_arr:
        if not nums:
            continue
        
        if len(nums) > 1:
            # Get the first and last numbers
            pairs.append((nums[0], nums[-1]))
        else:
            # Use the same and only number
            pairs.append((nums[0], nums[0]))
    return pairs

    
def get_sum_of_pairs(lines):
    # Get all the numbers only for each line
    str_num_arr = [re.findall(r'\d', line) for line in lines] # or use isDigit.
    
    # Group them in pairs yo
    pairs = group_pairs(str_num_arr)
    
    # Sum the tuple pairs:
    return [int(pair[0] + pair[1]) for pair in pairs]



def get_word_sum_pairs(lines):
    number_map = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    
    converted_lines = []
    
 
    # Debug discrepancies by slicing and summing the pair arrays.


    # THis leads to the wrong total because conversion of each matching word is from left to right.
    # Could work if we went from right to left at the same time for last value.
    # for line in lines:
    #     converted_chars = []
    #     i = 0
    #     while i < len(line):
    #         found = False

    #         for idx, val in enumerate(number_map, 1):
    #             if line[i:].startswith(val):
    #                 converted_chars.append(str(idx))
    #                 i += len(val) 
    #                 found = True
    #                 break

    #         if not found:
    #             converted_chars.append(line[i])
    #             i += 1
        
    #     converted_lines.append(''.join(converted_chars))
    
 
    for line in lines:
        converted_chars, i = [], 0
        while i < len(line):
            char = line[i]
            found = None
            
            for idx, val in enumerate(number_map, 1):
                if line[i:].startswith(val):
                    found = str(idx)
                    break
            
            converted_chars.append(found if found else char)
            i += 1
        
        converted_lines.append(''.join(converted_chars))
        

    converted_lines2 = [
        ''.join([
            x if (x := ''.join([
                str(idx) for idx, val in enumerate(number_map, 1)
                if line[i:].startswith(val)
            ])) else line[i] 
            for i in range(len(line))
        ]) 
        for line in lines
    ]
     
    
    # This is a lookahead assertion. Ensuring that the pattern inside (...) starts at the current position, 
    # but doesn't consume characters (i.e., the match happens "in place" without advancing the position).  
    converted_lines3 = []
    for line in lines:
        converted_line = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
        new_line = ''
        for l in converted_line:
            for key in number_map.keys():
                l = l.replace(key, number_map[key])
            new_line += l
        converted_lines3.append(new_line)


    return get_sum_of_pairs(converted_lines3)


 
    
def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')

    sums = get_word_sum_pairs(lines)
    total_sum = sum(sums)
    
    print(total_sum)
 
    if 'input3.txt' in file_path: assert total_sum == 54100 
    if 'input2.txt' in file_path: assert total_sum == 54877 
        
    return total_sum
    

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)