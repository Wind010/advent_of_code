'''
--- Part Two ---

lookup takes:
inputs: A sequence of (start, length) tuples to process.
mapping: A string describing transformations between source and destination ranges.
It performs transformations using the following logic:

For each (start, length) in inputs, it processes the mapping entries.
Mapping Entries:
dst, src, len: Each entry specifies a destination start (dst), source start (src), and length (len).
If the current start lies within the src range (delta in range(len)), the range is transformed.
A new range (dst + delta, len) is generated, representing the mapped region.
If no mappings apply, the original range is yielded and processing stops for that range.
Key Operations:
Splitting Ranges: The range is split and transformed into mapped ranges iteratively.
Yield: The function generates results one at a time, preserving memory efficiency.
'''


from functools import reduce
from common.common import arg_parse, timer

@timer
def find_minimum_location(data):
    seeds, *mappings = data.split('\n\n')
    seeds = list(map(int, seeds.split()[1:]))

    def process(inputs, mapping):
        for start, length in inputs:
            while length > 0:
                for m in mapping.split('\n')[1:]:
                    dst, src, delta = map(int, m.split())
                    diff = start - src
                    if diff in range(delta):
                        delta = min(delta - diff, length)
                        yield (dst + diff, delta)
                        start += delta
                        length -= delta
                        break
                else: yield (start, length); break
 
    #print(list(zip(seeds, [1] * len(seeds))), list(zip(seeds[0::2], seeds[1::2])))
 
    # Inputs [(79, 1), (14, 1), (55, 1), (13, 1)] [(79, 14), (55, 13)]
    # Because we don't care about the reset of the ranges, we just care about the first seed start value
    # since it will map to the target minimum eventually.
    start, min_location = [min(reduce(process, mappings, s))[0] for s in [
        zip(seeds, [1] * len(seeds)),
        zip(seeds[0::2], seeds[1::2])]]

    return min_location

def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    
    min_location = find_minimum_location(data)
  
    if 'input1.txt' in file_path: assert min_location == 46
    if 'input2.txt' in file_path: assert min_location == 2520479


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

