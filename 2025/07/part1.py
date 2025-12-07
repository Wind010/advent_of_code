'''
https://adventofcode.com/2025/day7
'''


from common.common import arg_parse, assertions, timer
from collections import defaultdict


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Grid:
    def __init__(self, data):
        self.data = data
        self.height = len(data)
        self.width = len(data[0]) if data else 0

    @staticmethod
    def parse(input_str):
        lines = input_str.strip().splitlines()
        data = [list(line) for line in lines]
        return Grid(data)

    def find(self, value):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == value:
                    return Point(x, y)
        return None

    def __getitem__(self, point):
        return self.data[point.y][point.x]


def find_splits(input_str):
    grid = Grid.parse(input_str)
    start = grid.find('S')
    splits = 0
    # Current is tracking the ways to reach each x-coordinate in the current row
    # While next_map is for the next row and possible timelines
    current, next_map = defaultdict(int), defaultdict(int)
    
    current[start.x] = 1
    
    for y in range(1, grid.height):
        for x, count in list(current.items()):
            current[x] = 0  # Set as processed... this bug...
            if grid[Point(x, y)] == '^':
                splits += 1
                # Check those damn grid boundaries
                if x > 0:
                    next_map[x - 1] += count
                if x < grid.width - 1:
                    next_map[x + 1] += count
            else:
                next_map[x] += count
        current, next_map = next_map, defaultdict(int) # Swap maps for next row

    return (splits, sum(current.values()))



def main(args, data):
    splits, total = find_splits(data)
    
    assertions(args, splits, 21, 1687, 1537)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)


