'''
https://adventofcode.com/2024/day/11
'''


from common.common import arg_parse, assertions, timer


def blink(n):
    '''
    Time complexity:  O(k) where k is the number of digits in n.  In the worst case could be log(n).
    '''
    s = str(n)
    if n == 0:
        return [1]
    elif len(s) % 2 == 0:
        mid = len(s) // 2
        divided_split = [int(s[:mid]), int(s[mid:])]
        if all(d == 0 for d in divided_split):
            return [0]
        else:
            return divided_split
    else:
        return [n * 2024]


@timer
def blink_iterative(numbers, times):
    '''
    Time complexity:  O(t * m * n)
    '''
    while times > 0:
        stones = []
        for n in numbers:
            stones.extend(blink(n))
        numbers = stones
        times -= 1
        #print(times, numbers)
        print(times)
    return numbers


@timer
def blink_recursive(numbers, times):
    '''
    Time complexity:  O(t * m * n)
    '''
    if times == 0:
        #print(len(numbers))
        return numbers
    
    stones = []
    for n in numbers:
       stones.extend(blink(n))
    
    #print(times, stones)
    return blink_recursive(stones, times-1)
    
        


def main(args, data):
    line = data.strip().split(' ')
    numbers = list(map(int, line))
    
    TIMES = 25
    
    stones1 = blink_recursive(numbers, TIMES)
    num_stones2 = len(stones1)
    stones2 = blink_iterative(numbers, TIMES)
    num_stones2 = len(stones2)
    
    assert num_stones2 == num_stones2

    assertions(args, num_stones2, 55312, 202019) #204022

    return stones1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

