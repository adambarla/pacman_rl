
from utils.constants import Direction


def is_wall(tile, maze):
    assert type(tile[0]) == int, "Position x must be an integer"
    assert type(tile[1]) == int, "Position y must be an integer"
    assert in_bounds(tile, maze), "Position out of bounds"
    if maze[tile[1]][tile[0]] == 1:
        return True
    return False

def in_bounds(tile, maze):
    assert type(tile[0]) == int, "Position x must be an integer"
    assert type(tile[1]) == int, "Position y must be an integer"

    w = len(maze[0])
    h = len(maze)
    if tile[0] < 0 or tile[0] >= w:
        return False
    if tile[1] < 0 or tile[1] >= h:
        return False
    return True


def can_turn(dir, new_dir):
    if not dir:
        return True
    if new_dir == Direction.LEFT and dir == Direction.RIGHT \
        or new_dir == Direction.RIGHT and dir == Direction.LEFT \
        or new_dir == Direction.UP and dir == Direction.DOWN \
        or new_dir == Direction.DOWN and dir == Direction.UP:
        return False
    return True


def move(tile, dir, maze):
    if not dir:
        return tile
    if dir == Direction.LEFT:
        new_pos = (tile[0] - 1, tile[1])
    if dir == Direction.RIGHT:
        new_pos = (tile[0] + 1, tile[1])
    if dir == Direction.UP:
        new_pos = (tile[0], tile[1] - 1)
    if dir == Direction.DOWN:
        new_pos = (tile[0], tile[1] + 1)
    new_pos = teleport(new_pos, maze)
    return new_pos


def action(tile, dir, new_dir, maze):
    """
    I am at tile, and I want to move in dir.
    """
    if new_dir and can_turn(dir, new_dir) \
        and not is_wall(move(tile, new_dir, maze), maze):
        dir = new_dir
    new_tile = move(tile, dir, maze)
    if is_wall(new_tile, maze):
        return tile, None
    return new_tile, dir


def teleport(tile, maze):
    w = len(maze[0])
    h = len(maze)
    if tile[0] < 0:
        tile = (w + tile[0], tile[1])
    if tile[0] >= len(maze[0]):
        tile = (tile[0] - w, tile[1])
    if tile[1] < 0:
        tile = (tile[0], h + tile[1])
    if tile[1] >= len(maze):
        tile = (tile[0], tile[1] - h)
    return tile
