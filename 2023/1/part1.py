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


def validate():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths = [os.path.join(current_dir, f) for f in ["input1.txt", "input2.txt"] ]
    all_lines = [open(f, 'r', encoding='utf-8').read().split('\n') for f in file_paths]
    
    expected_results = [142, 54877]
    for i, lines in enumerate(all_lines):
        sums = get_sum_of_pairs(lines)
        total_sum = sum(sums)

        assert total_sum == expected_results[i]


def main(file_path):
    if 'txt' not in file_path:
        validate()
        return
    
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')
    sums = get_sum_of_pairs(lines)
    total_sum = sum(sums)
    
    print(sums)
    print(total_sum)

    if 'input1.txt' in file_path: assert total_sum == 142 
    if 'input2.txt' in file_path: assert total_sum == 54877 

    return total_sum
    

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)