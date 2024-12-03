'''
--- Part Two ---
As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?
'''



import re
from common.common import arg_parse, timer

DONT = '🚫'
DO = '🚀'

@timer
def correct_memory_multiply_regex_match(line):
    matches = re.findall(fr"(mul\((\d+),(\d+)\)|{DONT}|{DO})", line)
    print(matches)
    
    valid = [n for m in matches for n in m  if n]
    res, skip = [], False
    for prev, cur in zip(valid, valid[1::]):
        #print(prev, cur)
        if prev.isnumeric() and cur.isnumeric() and not skip:
            res.append((int(prev), int(cur)))
        if DONT in {prev, cur}:
            skip = True
        if DO in {prev, cur}:
            skip = False
            
    return res

@timer
def correct_memory_multiply_regex_match2(line):
    pattern = rf"(mul\((\d+),(\d+)\)|{DONT}|{DO})"
    matches = re.findall(pattern, line)

    res, ok_to_process = [], True
    for m in matches:
        #print(m)
        a, b, c = m
        if ok_to_process and b and c:
            res.append((int(c), int(b)))
            continue
        if m[0] == DO:
            ok_to_process = True
        elif m[0] == DONT:
            ok_to_process = False

    return res

@timer
def correct_memory_multiply_regex_match3(line):
    pattern = rf"(mul\((\d+),(\d+)\)|{DONT}|{DO})"
    matches = re.findall(pattern, line)
    ok_to_process = True 
    # Walrus operator baby!
    return [(int(c), int(b)) for a, b, c in matches 
            if (ok_to_process := (ok_to_process or a == DO) and not a == DONT) and b and c]


@timer
def correct_memory_multiply_regex_iterator(line):
    pattern = r'(?P<mul>mul\((?P<num1>\d+),(?P<num2>\d+)\))|(?P<action>🚫|🚀)' # Use named capture groups 
    matches = re.finditer(pattern, line)
    res, ok_to_process = [], True
    for match in matches:
        if match.group('mul'):
            if ok_to_process:
                num1 = int(match.group('num1'))
                num2 = int(match.group('num2'))
                res.append((num1, num2))
        elif match.group('action'):
            if match.group('action') == DONT:
                ok_to_process = False
            elif match.group('action') == DO:
                ok_to_process = True

    return res



def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    line = data.strip().replace('\n', '').replace("don't()", DONT).replace("do()", DO)
    
    res = correct_memory_multiply_regex_match(line)
    total1 = sum(a * b for a, b in res)
    print(total1)

    res = correct_memory_multiply_regex_match2(line)
    total2 = sum(a * b for a, b in res)
    print(total1)

    res = correct_memory_multiply_regex_match3(line)
    total3 = sum(a * b for a, b in res)
    print(total1)

    res = correct_memory_multiply_regex_iterator(line)
    multi_pair = [(int(a) * int(b)) for a, b in res]
    total4 = sum(multi_pair)
    print(total2)
 

    assert total1 == total2 == total3 == total4
    if 'input3.txt' in file_path: assert total1 == 48
    if 'input2.txt' in file_path: assert total1 == 94455185
 


if __name__ == "__main__":
    args = arg_parse(__file__, 'input3.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

