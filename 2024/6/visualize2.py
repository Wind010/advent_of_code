from constants import *
import os

#from part1 import find_guard_and_obstacles

def read_grid_from_file(file_path):
    """Reads a grid from a file and returns it as a list of lists."""
    grid = []
    with open(file_path, "r") as file:
        for line in file:
            grid.append([i for i in line.strip().replace(OBSTACLE, RENDER_OBSTACLE)])
    return grid

def get_color(value, render_type):
    if render_type == 1:
        return get_gradient_color(value)
    return get_directional_color(value)


def get_gradient_color(value):
    """Returns an ANSI color code based on the value."""
    normalized_value = value % 360
    if normalized_value < 120:
        r = 255 - (normalized_value * 255 // 120)
        g = (normalized_value * 255 // 120)
        b = 0
    elif normalized_value < 240:
        r = 0
        g = 255 - ((normalized_value - 120) * 255 // 120)
        b = ((normalized_value - 120) * 255 // 120)
    else:
        r = ((normalized_value - 240) * 255 // 120)
        g = 0
        b = 255 - ((normalized_value - 240) * 255 // 120)
    return f"38;2;{r};{g};{b}"


def get_directional_color(value):
    if value == 0:
        color = (0, 0, 255)  # Blue
    elif value == 1:
        color = (255, 0, 0)  # Red
    elif value == 2:
        color = (0, 255, 0)  # Green
    elif value == 3:
        color = (255, 255, 0)  # Yellow
    else:
        color = (128, 128, 128)  # Gray (or any other default color)
    
    r, g, b = color    
    return f"38;2;{r};{g};{b}"



def move_guard(grid, guard, current_direction, visited_cells, render_type = 0):
    """Moves the guard in the specified direction if possible."""
    x, y = guard
    current_cell = grid[x][y]
    count = len(visited_cells)
    
    def get_colored_cell(count, direction):
        value = direction if render_type == 0 else count
        return f"\x1b[{get_color(value, render_type)}m{STEP}\x1b[0m"

    
    print(f"Current position: ({x}, {y}), Direction: {current_direction}, with value {current_cell}, Count: {count}")

    if current_cell in DIRECTIONS:
        # Should happen once and all others are '.'
        dx, dy = DIRECTIONS[current_cell]
        new_x, new_y = x + dx, y + dy
        
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] != RENDER_OBSTACLE:
            grid[x][y] = get_colored_cell(count, current_direction)
            guard = (new_x, new_y)
            visited_cells.add(guard)
    else:
        print(f"Moving in {list(DIRECTIONS.keys())[0]} at ({x}, {y}): {current_cell}")
        directions_list = list(DIRECTIONS.values())
        dx, dy = directions_list[current_direction]
        new_x, new_y = x + dx, y + dy
        
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
            
            if grid[new_x][new_y] == RENDER_OBSTACLE:
                new_dir_tuple = directions_list[(current_direction + 1) % len(directions_list)]
                new_direction = directions_list.index(new_dir_tuple)
                print(f"Obstacle encountered at ({x}, {y}). Changing direction to {new_direction}")
                dx, dy = new_dir_tuple
                new_x, new_y = x + dx, y + dy
                grid[new_x][new_y] = get_colored_cell(count, new_direction)
                return guard, visited_cells, new_direction, True
            else:
                print(f"Moved to position: ({guard[0]}, {guard[1]}), New Direction: {current_cell}, Count: {count}")
                guard = (new_x, new_y)
                grid[new_x][new_y] = get_colored_cell(count, current_direction)
                count += 1
                visited_cells.add(guard)
                return guard, visited_cells, current_direction, True
        else:
            return guard, visited_cells, current_direction, False

    
    print(f"Moved to position: ({guard[0]}, {guard[1]}), New Direction: {current_cell}, Count: {count}")
    return guard, visited_cells, current_direction, True


def print_grid(grid):
    """Prints the grid to the console."""
    for row in grid:
        print("".join(row))
    print()


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "input_visual_1.txt")
    grid = read_grid_from_file(file_path)
    guard = [(x, row.index(GUARD)) for x, row in enumerate(grid) if GUARD in row][0]

    running, current_dir, visited = True, 0, set()
    try:
        while running:
            guard, visited, current_dir, moved = move_guard(grid, guard, current_dir, visited)
            if not moved or guard[0] < 0 or guard[0] >= len(grid) or guard[1] < 0 or guard[1] >= len(grid[0]):
                running = False
    except KeyboardInterrupt:
        print(guard)

    grid[guard[0]][guard[1]] = '\033[42m' + "🥷" + "\033[0m"
    print_grid(grid)
    print(len(visited))


if __name__ == "__main__":
    main()