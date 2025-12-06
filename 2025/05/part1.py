'''
https://adventofcode.com/2025/day5
'''


from common.common import arg_parse, assertions, timer


def find_fresh_ids(fresh_range, ids):
    fresh_ids = []
    for id in ids:
        for r in fresh_range:
            if id in r:
                fresh_ids.append(id)
                break
    return fresh_ids
    # return [id for id in ids if any(id in r for r in fresh_range)]

def main(args, data):
    #lines = [line for line in data.strip().split('\n') if line]
    lines = data.strip().split('\n')
    total = 0
    fresh_range, ids = set(), []
    for line in lines:
        if not line:
            continue
        if '-' in line:
            start, end = map(int, line.split('-'))
            fresh_range.add(range(start, end + 1))
        else:
            ids.append(int(line))
            
    total = len(find_fresh_ids(fresh_range, ids))

    assertions(args, total, 3, 601, 640)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
