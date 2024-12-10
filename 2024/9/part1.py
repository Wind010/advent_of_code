'''
https://adventofcode.com/2024/day/9
'''


import re
from common.common import arg_parse, assertions, timer
from  multiprocessing import Pool, cpu_count
import itertools

DOT = '.'

@timer
def defrag_original(data):
    ''' Time complexity of O(f*fs + k + cb) where k is free space not defragmented and cb are actual contiguous blocks.'''
    #disk_map = dict(zip(data[::2], data[1::2]))
    blocks, file_id = [], 0
    for i in range(0, len(data) - 1, 2):
        files = data[i]
        free_space = data[i + 1]
        blocks.extend([str(file_id)] * int(files))
        blocks.extend([DOT] * int(free_space))
        file_id += 1

    # Handle the case where there is an unpaired file size at the end
    if len(data) % 2 != 0:
        blocks.extend([str(file_id)] * int(data[-1]))
        file_id += 1


    i, j = 0, len(blocks) - 1
    while i < len(blocks):
        while i < j and blocks[j] == DOT:
            j -= 1
        
        if i < j and blocks[i] == DOT:
            #print(i, j, blocks[i], blocks[j] )
            blocks[i], blocks[j] = blocks[j], blocks[i]
            # XOR
            # a = a ^ b
            # b = b ^ a
            # a = a ^ b
        i += 1

    
    #blocks = ''.join(blocks)
    #print(blocks, i, j)
    #nums = blocks.replace(DOT, '')

    checksums, j = [], 0
    for d in blocks:
        if d == DOT:
            break
        checksums.append(j * int(d))
        #checksums += j * int(d)
        #print(f"{j}*{int(d)}={j * int(d)}")
        j += 1
    
    return checksums


@timer
def defrag_cleaner_but_slower(data):
    ''' 
    Time complexity of O(f*fs + k*b + cb) where k is free space not defragmented and cb are actual contiguous blocks.
    Where b is the iteration through blocks looking for the next index of DOT.
    '''
    # Populate as original, but using file ID as every even number starting wtih 0.
    blocks = [i//2 if i%2 == 0 else DOT for i, num in enumerate(data) for _ in range(int(num))]

    while DOT in blocks:
        if blocks[-1] == DOT:
            blocks.pop() # Just throw it away
        else:
            index = blocks.index(DOT) # Adds another loop each time through blocks.
            blocks[index] = blocks.pop()
    
    return [i * num for i, num in enumerate(blocks)]


@timer
def defrag_cleaner_and_faster(data):
    ''' Time complexity of O(f*fs + k + cb) where k is free space not defragmented and cb are actual contiguous blocks.'''
    blocks = [i // 2 if i % 2 == 0 else DOT for i, num in enumerate(data) for _ in range(int(num))]

    i, j = 0, len(blocks) - 1
    while i < len(blocks):
        while i < j and blocks[j] == DOT:
            j -= 1
        if i < j and blocks[i] == DOT:
            blocks[i], blocks[j] = blocks[j], blocks[i]
        i += 1
 
    return [i * num for i, num in enumerate(blocks) if num != DOT]


def main(args, data):
    data = data.strip()

    checksum1 = sum(defrag_original(data))
    checksum2 = sum(defrag_cleaner_and_faster(data))
    checksum3 = sum(defrag_cleaner_but_slower(data))
    assert checksum1 == checksum2 == checksum3
    
    assertions(args, checksum1, 1928, 6398252054886)

    return checksum1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)

