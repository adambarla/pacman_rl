
TILE_SIZE = 32

class Direction:
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP = 4

def is_wall(pos, maze):
    assert in_bounds(pos, maze), "Position out of bounds"
    if maze[pos[1]][pos[0]] == 1:
        return True
    return False

def in_bounds(pos, maze):
    w = len(maze[0])
    h = len(maze)
    if pos[0] < 0 or pos[0] >= w:
        return False
    if pos[1] < 0 or pos[1] >= h:
        return False
    return True


def try_turning(pos, dir, new_dir, maze):
    if not new_dir:
        return dir, None
    new_pos = move(pos, new_dir, maze)
    if is_wall(new_pos, maze) \
        or new_dir == Direction.LEFT and dir == Direction.RIGHT \
        or new_dir == Direction.RIGHT and dir == Direction.LEFT \
        or new_dir == Direction.UP and dir == Direction.DOWN \
        or new_dir == Direction.DOWN and dir == Direction.UP:
        return dir, new_dir
    return new_dir, None

def move(pos, dir, maze):
    assert in_bounds(pos, maze), "Position out of bounds"
    if not dir:
        return pos
    if dir == Direction.LEFT:
        new_pos = (pos[0] - 1, pos[1])
    if dir == Direction.RIGHT:
        new_pos = (pos[0] + 1, pos[1])
    if dir == Direction.UP:
        new_pos = (pos[0], pos[1] - 1)
    if dir == Direction.DOWN:
        new_pos = (pos[0], pos[1] + 1)
    return teleport(new_pos, maze)

def update(pos, dir, maze):
    new_pos = move(pos, dir, maze)
    if is_wall(new_pos, maze):
        return pos, None
    return new_pos, dir
    

def teleport(pos, maze):
    w = len(maze[0])
    h = len(maze)
    if pos[0] < 0:
        pos = (w - 1, pos[1])
    if pos[0] >= w:
        pos = (0, pos[1])
    if pos[1] < 0:
        pos = (pos[0], h - 1)
    if pos[1] >= h:
        pos = (pos[0], 0)
    return pos

