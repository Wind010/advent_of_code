'''
https://adventofcode.com/2024/day/11
'''


from common.common import arg_parse, assertions, timer
from multiprocessing import Pool, cpu_count
from functools import cache
from part1 import blink
import math
from collections import defaultdict


def chunk(numbers, n):
    '''
    Time complexity:  
    '''
    k, m = divmod(len(numbers), n)
    return [numbers[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

 

# def blink_multiprocess_iterative(numbers, times, num_processes=None):
#     if num_processes is None:
#         num_processes = cpu_count()

#     chunk_size = 8
#     chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]
    
#     with Pool(num_processes) as pool:
#         results = pool.starmap(blink_iterative, [(chunk, times) for chunk in chunks])

#     return [item for sublist in results for item in sublist]


# @timer
# def blink_multiprocess_iterative(numbers, times, num_processes=None):
#     if num_processes is None:
#         num_processes = cpu_count()

#     for _ in range(times):

#         chunk_size = 8 #(len(numbers) + num_processes - 1) // num_processes
#         chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]
        
#         with Pool(num_processes) as pool:

#             results = pool.map(blink_iterative, chunks)
        
#         numbers = [item for sublist in results for item in sublist]
    
#     return numbers



# @timer
# def blink_multiprocess_iterative(numbers, times, num_processes=None):
#     if num_processes is None:
#         num_processes = cpu_count()

#     from datetime import datetime
#     start_time = datetime.now()
    
#     pool = Pool(num_processes)
#     try:
#         for t in range(times, 0, -1):
#             chunk_size = 32 #(len(numbers) + num_processes - 1) // num_processes
#             chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]
            
#             #print(t, chunks)
            
#             results = pool.map(blink_iterative, chunks)
#             numbers = [item for sublist in results for item in sublist]
            
#             end_time = datetime.now()
#             elapsed_time = end_time - start_time
#             print(t, elapsed_time)
#     finally:
#         pool.close()
#         pool.join()

#     return numbers





#@timer
def blink_recursive(n, times, memo):
    key =  (n, times)
    if key in memo:
        return memo[key]
    
    times -= 1

    if times == -1:
        result = 1
    elif n == 0:
        result = blink_recursive(1, times, memo)
    else:
        s = str(n)
        if len(s) % 2 == 0:
            mid = len(s) // 2
            left_half, right_half = int(s[:mid]), int(s[mid:])
            result = blink_recursive(left_half, times, memo) + blink_recursive(right_half, times, memo)
        else:
            result = blink_recursive(n * 2024, times, memo)

    memo[key] = result
    return result


@timer
def blink_recursive_run(numbers, times):
    memo = {}
    return [blink_recursive(n, times, memo) for n in numbers]


def blink_iterative_run(numbers, times):
    memo = {}
    res = []
    for n in numbers:
        res.append(blink_iterative(n, times, memo))
    return res



def tens(n: int) -> int:
  ''' Faster way to count digits without casting to string '''
  return int(math.log10(n)) + 1


@cache
def blink_cache(n, times):
    if times == 0:
        return 1
    
    times -= 1
    if n == 0:
        return blink_cache(1, times)

    if (digits:= tens(n)) % 2 == 0:
        numbers = list(divmod(n, 10 ** (digits // 2)))
        return sum([blink_cache(n, times) for n in numbers])
    
    return blink_cache(n * 2024, times)


@timer
def blink_cache_run(numbers, times):
    return [blink_cache(n, times) for n in numbers]


@cache
def blink_cache2(n, times=75):
    if times == 0: 
        return 1
    
    times -= 1
    if n == 0: 
        return blink_cache2(1, times)

    digits = tens(n)
    if digits % 2: 
        return blink_cache2(n * 2024, times)

    return (blink_cache2(n // 10**(digits//2), times) + blink_cache2(n %  10**(digits//2), times))



def blink_dict_counts(stones):
    '''
    Time complexity:  O(n log(m)) where n is the dictionary items and n is the max number of digits in each number.
    '''
    stonework = dict(stones)
    for stone, count in stonework.items():
        if count == 0:
            continue
        if stone == 0:
            stones[1] += count
            stones[0] -= count
        elif len(str(stone)) % 2 == 0:
            stone_str = str(stone)
            new_len = int(len(stone_str) // 2)
            stone_1 = int(stone_str[:new_len])
            stone_2 = int(stone_str[new_len:])
            stones[stone_1] += count
            stones[stone_2] += count
            stones[stone] -= count
        else:
            stones[stone * 2024] += count
            stones[stone] -= count
    return

@timer
def blink_dict_counts_run(numbers, times):
    stones = defaultdict(int)
    
    for n in numbers:
        stones[n] += 1
    
    for i in range(times):
        blink_dict_counts(stones)
        #print(i, len(stones))
    
    return stones


def main(args, data):
    line = data.strip().split(' ')
    numbers = list(map(int, line))
    
    TIMES = 75
    
    stone_counts1 = blink_recursive_run(numbers, TIMES)
    num_stones1 = sum(stone_counts1)
    
    stone_counts2 = blink_cache_run(numbers, TIMES)
    num_stones2 = sum(stone_counts2)
    
    num_stones3 = sum((map(blink_cache2, numbers)))
    
    stone_counts4 = blink_dict_counts(numbers, TIMES)
    num_stones4 = sum(stone_counts4.values())
    
    assert num_stones1 == num_stones2 == num_stones3 == num_stones4
    
    assertions(args, num_stones1, 65601038650482, 239321955280205)

    return num_stones1
    

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

