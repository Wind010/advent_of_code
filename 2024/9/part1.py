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
    #disk_map = dict(zip(data[::2], data[1::2]))
    # blocks, file_id = [], 0
    # for files, free_space in list(zip(data[::2], data[1::2])):
    #     blocks.extend(str(file_id) * int(files) + DOT * int(free_space))
    #     file_id += 1
    

    # if len(data) % 2 != 0:
    #     blocks += str(file_id) * int(data[-1])
    #     file_id += 1

    blocks = [i//2 if i%2 == 0 else DOT for i, num in enumerate(data) for _ in range(int(num))]


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
def defrag_clean(data):
    # Populate as original, but using file ID as every even number starting wtih 0.
    blocks = [i//2 if i%2 == 0 else DOT for i, num in enumerate(data) for _ in range(int(num))]
    v = blocks.copy()
    while DOT in blocks:
        if blocks[-1] == DOT:
            blocks.pop() # Just throw it away
        else:
            index = blocks.index(DOT)
            blocks[index] = blocks.pop()
    

    return [i * num for i, num in enumerate(blocks)]




def main(args, data):
    data = data.strip()

    checksum = sum(defrag_original(data))
    checksum = sum(defrag_clean(data))
    
    assertions(args, checksum, 1928, 6398252054886) 

    return checksum
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

