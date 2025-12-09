'''
https://adventofcode.com/2025/day9
'''

from shapely.geometry import box
# We need

from common.common import arg_parse, assertions, timer


def parse_input(data):
    #return [(map(int, (parts[0], parts[1]))) for line in data.splitlines() for parts in [line.split(',')]]
    #return [(int(line.split(',')[0]), int(line.split(',')[1])) for line in data.splitlines()]
    return list(map(lambda line: tuple(map(int, line.split(',')[:2])), data.splitlines()))

@timer
def find_largest_rectangle_area(red_tiles):
    max_area = 0
    for i, (x1, y1) in enumerate(red_tiles):
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]
            if x1 != x2 and y1 != y2:
                width = abs(x1 - x2) + 1 # Includes the tiles (inclusive).
                height = abs(y1 - y2) + 1 # Includes the tiles (inclusive).
                area = width * height
                if area > max_area:
                    max_area = area
    return max_area



def main(args, data):
    coords = parse_input(data)
    area = find_largest_rectangle_area(coords)

    assertions(args, area, 50, 4763509452, 4729332959)
    return area
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

