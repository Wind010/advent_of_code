'''
https://adventofcode.com/2024/day/12
'''


import re
from common.common import arg_parse, assertions, timer
from collections import defaultdict, deque


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)] 

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
            area, perimeter = 0, 0

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
                        # Were done since no matching plants in this cell.
                        perimeter += 1
                        
            plants[plant_type].append((area, perimeter))
 
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
    if 'input1.txt' in args.file_path: assert total_price == 140
    if 'input2.txt' in args.file_path: assert total_price == 772
    if 'input3.txt' in args.file_path: assert total_price == 1930
    if 'input4.txt' in args.file_path: assert total_price == 1451030
    if 'input5.txt' in args.file_path: assert total_price == 1467094
    
    return total_price
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
    args = arg_parse(__file__, 'input4.txt', main)
    args = arg_parse(__file__, 'input5.txt', main)
