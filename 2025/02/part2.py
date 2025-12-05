'''
https://adventofcode.com/2025/day2
'''


from common.common import arg_parse, assertions, timer


def find_invalid_id(start, end):
    t = 0
    for id in range(start, end+1):
        if is_invalid_id(id):
            t += int(id)
    return t
    
def is_invalid_id(num):
    str_num = str(num)
    length = len(str_num)

    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len != 0:
            continue

        pattern = str_num[:pattern_len]
        is_valid = True

        for i in range(0, length, pattern_len):
            if str_num[i:i + pattern_len] != pattern:
                is_valid = False
                break

        if is_valid:
            return True

    return False



def find_invalid_id_cleaner(start, end):
    '''Cleaner, but slower and less easy to parse.'''
    return sum(id for id in range(start, end + 1) if is_repeated_pattern(id))

def is_repeated_pattern(num):
    str_num = str(num)
    length = len(str_num)
    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len != 0:
            continue
        pattern = str_num[:pattern_len]
        if all(str_num[i:i + pattern_len] == pattern for i in range(0, length, pattern_len)):
            return True
    return False

            
def main(args, data):
    lines = data.strip().split(',')
    total1, total2 = 0, 0
    for ids in lines:
        start, end = map(int, ids.split('-'))
        total1 += find_invalid_id(start, end)
        total2 += find_invalid_id_cleaner(start, end)

    assertions(args, total1, 4174379265, 27469417404, 69553832684)
    assertions(args, total2, 4174379265, 27469417404, 69553832684)
    
    return total2
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

