'''

'''



import re
from common.common import arg_parse, assertions, timer
from collections import defaultdict
import heapq


def find_space(blanks, length):
    min_index, found_length = None, None
    for n in range(length, 10):
        li = blanks[n]
        if not li:
            continue
        i = li[0]
        if min_index is None or i < min_index:
            min_index = i
            found_length = n
    if min_index is None:
        return None
    heapq.heappop(blanks[found_length])
    if found_length > length:
        heapq.heappush(blanks[found_length - length], min_index + length)
    return min_index


@timer
def defrag_original(data):
    ''' 
    Time complexity of O(f*fs + O(f) + O(log fs) * O(fs) + f) where fs is the numer of elements in the heap tracking free space. 
    In worst case the heap could be O(log k) where k is the total number of unique free spaces (they all fit).
    The n is the numer of files.
    '''
    files = {}  # File start position: Size
    free_space = defaultdict(lambda: [])  # Length: Free space start positions

    file_id = 0
    for i, num in enumerate(map(int, data)):
        if i % 2 == 0:
            files[i//2] = [file_id, int(num)]
        elif num > 0:
                heapq.heappush(free_space[num], file_id)
        file_id += num

    # Sort the file_ids and iterate starting from the largest file Ids.
    for i in sorted(files.keys(), reverse=True):
        file_start, file_size = files[i]
        
        # Find free space large enough to fit the file
        possible_free_space = sorted([[free_space[fs_size][0],fs_size] 
                                      for fs_size in free_space if fs_size >= file_size])

        if possible_free_space:
            fs_start, fs_size = possible_free_space[0]
            if file_start > fs_start:
                files[i] = [fs_start,file_size]
                
                # Adjust free space.
                heapq.heappop(free_space[fs_size])
                if not free_space[fs_size]:
                    del free_space[fs_size]

                remaining_free_space_size = fs_size - file_size
                if remaining_free_space_size:
                    heapq.heappush(free_space[remaining_free_space_size], fs_start + file_size)
                

    return [num*(start * length + (length*(length-1)) // 2) for num, (start, length) in files.items()]


@timer
def defrag_optimized(data):
    ''' 
    Time complexity of O(f*fs + O(f) + O(log fs) *O(fs) + f) where fs is the numer of elements in the heap tracking free space. 
    In worst case the heap could be O(log k) where k is the total number of unique free spaces (they all fit).
    The n is the numer of files.
    '''
    files = {}  # File start position: Size
    free_space = defaultdict(lambda: [])  # Length: Free space start positions

    file_id = 0
    for i, num in enumerate(map(int, data)):
        if i % 2 == 0:
            files[i//2] = [file_id, int(num)]
        elif num > 0:
                heapq.heappush(free_space[num], file_id)
        file_id += num

    # Sort the file_ids and iterate starting from the largest file Ids.
    for i in sorted(files.keys(), reverse=True):
        file_start, file_size = files[i]
        
        # Find free space large enough to fit the file
        possible_free_space = [
            (start, size) for size, starts in free_space.items() if size >= file_size for start in starts
        ]
        
        if possible_free_space:
            fs_start, fs_size = min(possible_free_space, key=lambda x: x[0])  # Get the smallest start index
            if file_start > fs_start:
                files[i] = [fs_start,file_size]

                # Adjust free space.
                heapq.heappop(free_space[fs_size])
                if not free_space[fs_size]:
                    del free_space[fs_size]

                remaining_free_space_size = fs_size - file_size
                if remaining_free_space_size:
                    heapq.heappush(free_space[remaining_free_space_size], fs_start + file_size)
                

    return [num*(start * length + (length*(length-1)) // 2) for num, (start, length) in files.items()]


def main(args, data):
    data = data.strip()

    checksum1 = sum(defrag_original(data))
    checksum2 = sum(defrag_optimized(data))
    
    assert checksum1 == checksum2
    assertions(args, checksum1, 2858, 6415666220005) #6307279963620

    return checksum1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

