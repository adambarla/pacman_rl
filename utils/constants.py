class Tile:
    EMPTY = 0
    WALL = 1
    COIN = 2
    POWERUP = 3


class Direction:
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP = 4


class Phase:
    SCATTER = 1
    CHASE = 2
    FRIGHTENED = 3
    EATEN = 4


PLAYER_PLAYING = False
CONTINUOUS = True
DRAW_PERIOD = 1000

TILE_SIZE = 16
OFFSET = 1

TICK_PER_SECOND = 60
TICK_TIME = 1000 / TICK_PER_SECOND
SCATTER_SECONDS = 7
CHASE_SECONDS = 20
SPEED_PER_SECOND = 7.5
NEW_GHOST_WAIT = 7  # seconds

REWARD_SURVIVED = 0
REWARD_PER_COIN = 1
REWARD_PER_POWERUP = 50
REWARD_FOR_DEATH = -100
REWARD_PER_KILL = 200


ACTIONS = [Direction.LEFT, Direction.DOWN, Direction.RIGHT, Direction.UP]

GHOST_COLORS = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 81)]


MAZE = [
    "============================",
    "=............||............=",
    "=.||||.|||||.||.|||||.||||.=",
    "=o||||.|||||.||.|||||.||||o=",
    "=.||||.|||||.||.|||||.||||.=",
    "=..........................=",
    "=.||||.||.||||||||.||.||||.=",
    "=.||||.||.||||||||.||.||||.=",
    "=......||....||....||......=",
    "======.||||| || |||||.======",
    "======.||||| || |||||.======",
    "======.||    G     ||.======",
    "======.|| |||--||| ||.======",
    "======.|| |      | ||.======",
    "      .   | DDDD |   .      ",
    "======.|| |      | ||.======",
    "======.|| |||||||| ||.======",
    "======.||          ||.======",
    "======.|| |||||||| ||.======",
    "======.|| |||||||| ||.======",
    "=............||............=",
    "=.||||.|||||.||.|||||.||||.=",
    "=.||||.|||||.||.|||||.||||.=",
    "=o..||.......S........||..o=",
    "=||.||.||.||||||||.||.||.||=",
    "=||.||.||.||||||||.||.||.||=",
    "=......||....||....||......=",
    "=.||||||||||.||.||||||||||.=",
    "=.||||||||||.||.||||||||||.=",
    "=..........................=",
    "============================",
]
