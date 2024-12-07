from collections import OrderedDict

GUARD = '^'
OBSTACLE = '#'
STEP = '░' # 'X'
RENDER_OBSTACLE = '█' # '#'


class Directions:
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'


DIRECTIONS = OrderedDict([
    (Directions.UP, (-1, 0)),
    (Directions.RIGHT, (0, 1)),
    (Directions.DOWN, (1, 0)),
    (Directions.LEFT, (0, -1))
])