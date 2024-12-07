import random

def generate_data_grid(num_lines, chars_per_line, hash_density=0.075):
    total_chars = num_lines * chars_per_line
    grid = ['.' for _ in range(total_chars)]
    
    caret_index = random.randint(0, total_chars - 1)
    grid[caret_index] = '^'
    
    num_hashes = int(total_chars * hash_density)
    
    if num_hashes > 0:
        hash_indices = random.sample(range(total_chars), num_hashes)
        for index in hash_indices:
            if grid[index] != '^':  # Ensure '^' is not overwritten
                grid[index] = '#'

    formatted_grid = '\n'.join([''.join(grid[i * chars_per_line:(i + 1) * chars_per_line]) for i in range(num_lines)])
    
    return formatted_grid


num_lines = 25
chars_per_line = 50 

grid = generate_data_grid(num_lines, chars_per_line)
print(grid)