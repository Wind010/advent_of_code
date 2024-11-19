# https://adventofcode.com/2023/day/1

'''
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

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

import argparse
import os
import re


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
    sums = get_sum_of_pairs(lines)
    total_sum = sum(sums)
    

    sums2 = get_word_sum_pairs(lines)
    total_sum2 = sum(sums2)
    
    print(sums)
    print(total_sum)
    print(sums2)
    print(total_sum2)
    
    if 'input1.txt' in file_path: assert total_sum == 142 
    if 'input2.txt' in file_path: assert total_sum == 54877 
    if 'input3.txt' in file_path: assert total_sum2 == 54100 
    
    return (total_sum, total_sum2)
    

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_file_path = os.path.join(current_dir, 'input2.txt')
    
    parser = argparse.ArgumentParser(description="🖖")
    parser.add_argument("file_path", type=str, nargs='?', 
        default=default_file_path, help="The path to the file containing the input data.")
    args = parser.parse_args()
    
    main(args.file_path)
		