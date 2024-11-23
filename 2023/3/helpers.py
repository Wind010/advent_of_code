

DOT = '.'
ASTERISK = "*"
SYMBOLS = set('!@#$%^&*()-+?_=,<>/"')


DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
    (0, -1),         (0, 1),     # Left, Right
    (1, -1), (1, 0), (1, 1)      # Bottom-left, Bottom, Bottom-right
]

# Generate all possible directions for the surrounding cells.  Just use the hardcoded DIRECTIONS.
def generate_directions(matrix, x, y):
    directions = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:  # Exclude the center cell (0, 0)
                directions.append((dx, dy))
                
    return directions


# Could be Cell with x,y and Number, but this makes more sense for our purpose.
class Number:
    def __init__(self):
        self.pos = []
        self.value = 0