'''
https://adventofcode.com/2024/day/12
'''


import re
from common.common import arg_parse, assertions, timer
from collections import defaultdict, deque


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)] 

def find_fence_sides(sides, grid):
    unique_sides = 0
    for _, positions in sides.items():
        seen_perimeter = set()
        for pr, pc in positions:
            if (pr, pc) not in seen_perimeter:
                unique_sides += 1
                queue = deque([(pr, pc)])
                
                while queue:
                    row, col = queue.popleft()
                    #print(grid[row][col], row, col)
                    
                    if (row, col) in seen_perimeter:
                        continue
                    
                    seen_perimeter.add((row, col))
                    
                    # queue.extend((next_row, next_col) for dr, dc in DIRECTIONS
                    #            if (next_row := r2 + dr, next_col := c2 + dc) in positions)
                    
                    for dr, dc in DIRECTIONS:
                        next_row, next_col = row + dr, col + dc
                        if (next_row, next_col) in positions:
                            queue.append((next_row, next_col))
                            
    return unique_sides


@timer
def find_fence_price(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    plants = defaultdict(list)
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue
        
            plant_type = grid[r][c]
            #print(plant_type)
            
            queue = deque([(r, c)])
            area, sides  = 0, 0
            boundaries = dict()
            
            # Explore the current region with BFS
            while queue:
                row, col = queue.popleft()
                if (row, col) in visited:
                    continue
                visited.add((row, col))
                area += 1
                
                # Check all neighboring cells
                for dr, dc in DIRECTIONS:
                    next_row, next_col = row + dr, col + dc
                    if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] == grid[row][col]:
                        queue.append((next_row, next_col))
                    else:
                        boundaries.setdefault((dr, dc), set()).add((next_row, next_col))

            sides += find_fence_sides(boundaries, grid)
            plants[plant_type].append((area, sides))

    return plants
    
    
    

def main(args, data):
    garden = data.strip().split('\n')

    plants = find_fence_price(garden)
    #total_price = sum(area * perimeter for area, perimeter in [area_and_perim[-1] 
    #                                                           for area_and_perim in plants.values()])
    
    total_price = 0
    for area_and_perim in plants.values():
        for area, perimeter in area_and_perim:
            total_price += (area * perimeter)
    
            
    print(total_price)
    if 'input1.txt' in args.file_path: assert total_price == 80
    if 'input2.txt' in args.file_path: assert total_price == 436
    if 'input3.txt' in args.file_path: assert total_price == 1206
    if 'input6.txt' in args.file_path: assert total_price == 236
    if 'input7.txt' in args.file_path: assert total_price == 368
    if 'input4.txt' in args.file_path: assert total_price == 859494
    if 'input5.txt' in args.file_path: assert total_price == 881182
    
    return total_price
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input6.txt', main)
    args = arg_parse(__file__, 'input7.txt', main)
    args = arg_parse(__file__, 'input4.txt', main)
    args = arg_parse(__file__, 'input5.txt', main)
