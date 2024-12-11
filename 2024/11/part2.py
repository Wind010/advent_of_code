'''
https://adventofcode.com/2024/day/11
'''


from common.common import arg_parse, assertions, timer
from multiprocessing import Pool, cpu_count



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
    elif len(str(n)) % 2 == 0:
        s = str(n)
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


def main(args, data):
    line = data.strip().split(' ')
    numbers = list(map(int, line))
    
    TIMES = 75
    
    stone_counts = blink_recursive_run(numbers, TIMES)
    num_stones = sum(stone_counts)
    
    assertions(args, num_stones, 65601038650482, 239321955280205)

    return num_stones
    

if __name__ == "__main__":
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

