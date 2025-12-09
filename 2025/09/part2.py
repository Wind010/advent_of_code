'''
https://adventofcode.com/2025/day9

'''


# Looks like flood fill problem?  With so many points, it might take awhile.
# Either that or calcualte all rectangles and check the largest one that fits in that rectangle?

from part1 import parse_input
from common.common import arg_parse, assertions, timer


from itertools import combinations
from itertools import combinations, compress, starmap
from shapely import Polygon, box

# TODO:  Flood fill approach

@timer
def largest_rectangle_within_poly(red_tiles):
    area = area2 = 0
    poly = Polygon(red_tiles)

    for (x1, y1), (x2, y2) in combinations(red_tiles, 2):
        rect_size = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        area = max(rect_size, area)
        if rect_size < area2:
            continue

        # area is the anwer for part 1.
        
        rect = box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        # Covers vs contains to allow edges touching.  
        # For each of the rectangles, check if the polygon fully covers the rect.
        if poly.covers(rect):  
            area2 = max(rect_size, area2)
            
    return area2

@timer
def larget_rectangle_within_poly_clean(red_tiles):
    rects = [
        (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        for (x1, y1), (x2, y2) in combinations(red_tiles, 2)
    ]
    
    areas = [(x2 - x1 + 1) * (y2 - y1 + 1) for (x1, y1, x2, y2) in rects]
    
    # Part 1 would be max(areas)
    
    poly = Polygon(red_tiles)
    
    # Starmap to applies box to each tuple in rects.
    #[print(sm) for sm in starmap(box, rects)]
    
    # Filter areas that correspond to rectangles covered by the polygon via itertools.compress to speed up processing.
    return max(compress(areas, map(poly.covers, starmap(box, rects))))


def main(args, data):
    coords = parse_input(data)
    area = larget_rectangle_within_poly_clean(coords)

    assertions(args, area, 24, 1516897893, 1474477524)
    return area
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

