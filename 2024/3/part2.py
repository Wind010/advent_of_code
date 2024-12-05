'''
https://adventofcode.com/2024/day/3
'''



import re
from common.common import arg_parse, timer, assertions

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


def correct_memory_multiply_regex_sub_ropatel(line):
    sum, lineSum = 0, 0
    
    # Look for any matches in the STOP START block of the code, and remove
    pattern = r"(don't\(\).*?do\(\))"
    line = re.sub(pattern,'',line)

    # Look for any matches that follow a STOP without a START, and remove
    pattern = r"(don't\(\).*)"
    line = re.sub(pattern,'',line)

    # Let's see what the line looks like now.
    print(line)

    # Finally, let's find all the proper COMPUTE matches
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, line)

    # Iterate, compute and aggregate
    for x, y in matches:
        lineSum += int(x) * int(y)
        sum += int(x) * int(y)

    # Let's see what each line sum looks like 
    print("Line Sum = ", lineSum)
    print("\n")
    lineSum = 0
    
    # Print the final sum along with line count
    print("sum = ", sum)
    return sum
    

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



def main(args, data):
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
    
    line = data.strip().replace('\n', '')
    res1 = correct_memory_multiply_regex_sub_ropatel(line)

    assert total1 == total2 == total3 == total4 == res1

    assertions(args, total1, 48, 94455185)


if __name__ == "__main__":
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

