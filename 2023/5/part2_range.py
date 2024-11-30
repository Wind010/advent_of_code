'''
--- Part Two ---

'''

import math
import re
from common.common import arg_parse, timer
from dataclasses import *
import time


@dataclass
class Range:
    start: int
    end: int
    level: int

    @property
    def length(self):
        return self.end - self.start

    def overlaps(self, other):
        """Check if two ranges overlap."""
        return not (self.end <= other.start or other.end <= self.start)

    def split_at(self, position):
        """
        Split the range at the given position.
        Returns two ranges: one before the position, and one starting at the position.
        If position is not within the range, returns None for the non-existent range.
        """
        if position <= self.start:
            return None, self
        if position >= self.end:
            return self, None
        return Range(self.start, position, self.level), Range(position, self.end, self.level)

    def offset(self, diff):
        """Return a new Range shifted by diff and moved to the next level."""
        return Range(self.start + diff, self.end + diff, self.level + 1)


@timer
def find_min_clean(input):
    segments = input.split('\n\n')
    ranges = []
    for seed in re.findall(r'(\d+) (\d+)', segments[0]):
        start, length = map(int, seed)
        end = start + length
        ranges.append((start, end, 1))

    min_location = math.inf

    while ranges:
        #print(ranges[-1])
        start, end, level = ranges.pop() # Treat ranges like stack.
        if level == 8:
            min_location = min(start, min_location) # The incoming start is the lowest in that range.
            continue

        # Process mappings for the current level
        for mapping in re.findall(r'(\d+) (\d+) (\d+)', segments[level]):
            dest_start, source_start, length = map(int, mapping)
            source_end = source_start + length
            diff = dest_start - source_start
            if end <= source_start or source_end <= start:  # No overlap
                continue
            if start < source_start:    # Split original interval at source_start
                ranges.append((start, source_start, level))
                start = source_start
            if source_end < end:    # Split original interval at source_end
                ranges.append((source_end, end, level))
                end = source_end
                
            # Should now overlap completely and continue to next filter/level.
            ranges.append((start + diff, end + diff, level + 1)) 
            break
        else:
            ranges.append((start, end, level + 1))
  
    return min_location
        
@timer
def find_min_with_ranges(input):
    segments = input.split('\n\n')
    ranges = [Range(int(pair[0]), int(pair[0]) + int(pair[1]), 1) for pair in re.findall(r'(\d+) (\d+)', segments[0])]
    min_location = math.inf
    while ranges:
        #print(ranges[-1])
        current_range = ranges.pop()
        if current_range.level == 8:
            min_location = min(current_range.start, min_location)
            continue

        # Process mappings for the current level
        for mapping in re.findall(r'(\d+) (\d+) (\d+)', segments[current_range.level]):
            dest_start, source_start, length = map(int, mapping)
            source_range = Range(source_start, source_start + length, current_range.level)
            diff = dest_start - source_start
            if not current_range.overlaps(source_range):
                continue

            # Handle splitting and processing
            before_split, after_split = current_range.split_at(source_range.start)
            if before_split:
                ranges.append(before_split)
            if after_split:
                after_split, remaining = after_split.split_at(source_range.end)
                if remaining:
                    ranges.append(remaining)

            # Handle fully overlapping range
            if after_split:
                shifted_range = after_split.offset(diff)
                ranges.append(shifted_range)  # Should overlap completely.
            break
        else:
            # If no mappings matched, move to the next level
            ranges.append(Range(current_range.start, current_range.end, current_range.level + 1))
            
    return min_location
    


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')
    
    min_location = find_min_clean(data)
    
    if 'input1.txt' in file_path: assert min_location == 46
    if 'input2.txt' in file_path: assert min_location == 2520479

    min_location = find_min_with_ranges(data)
    
    if 'input1.txt' in file_path: assert min_location == 46
    if 'input2.txt' in file_path: assert min_location == 2520479


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)
