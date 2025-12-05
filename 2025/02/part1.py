'''
https://adventofcode.com/2025/day2
'''


from common.common import arg_parse, assertions, timer


def find_invalid_id(start, end):
    t = 0
    for id in range(start, end+1):
        id_str = str(abs(id))

        # Looks like it must be even length in examples for invalid IDs.
        if len(id_str) % 2 != 0:
            continue
        
        # if len(set(id_str)) != len(id_str):
        #     t += int(id)
        #     print(id)
        # if find_repeating_sequences(id):
        #     t += int(id)
        #     #print(id)
        
        half_len = len(id_str) // 2
        first = id_str[:half_len]
        second = id_str[half_len:]
        
        if first == second:
            t += int(id)
        
    return t

def find_repeating_sequences(number):
    digits = str(abs(number))
    n, repeats = len(digits), set()
    # Need atleast 2 repeating digits.
    for length in range(2, n):
        seen = set()
        for i in range(n - length + 1):
            seq = digits[i:i+length]
            if seq in seen:
                repeats.add(seq)
            else:
                seen.add(seq)
    return len(repeats) > 0

        
def main(args, data):
    lines = data.strip().split(',')
    total = 0
    for ids in lines:
        start, end = map(int, ids.split('-'))
        total += find_invalid_id(start, end)


    assertions(args, total, 1227775554, 16793817782, 53420042388)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

