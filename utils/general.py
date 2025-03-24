from utils.constants import Direction, Tile


def is_wall(tile, maze):
    assert type(tile[0]) == int, "Position x must be an integer"
    assert type(tile[1]) == int, "Position y must be an integer"
    assert in_bounds(tile, maze), "Position out of bounds"
    if maze[tile[1]][tile[0]] == Tile.WALL:
        return True
    return False


def is_coin(tile, maze):
    assert type(tile[0]) == int, "Position x must be an integer"
    assert type(tile[1]) == int, "Position y must be an integer"
    assert in_bounds(tile, maze), "Position out of bounds"
    if maze[tile[1]][tile[0]] == Tile.COIN:
        return True
    return False


def is_powerup(tile, maze):
    assert type(tile[0]) == int, "Position x must be an integer"
    assert type(tile[1]) == int, "Position y must be an integer"
    assert in_bounds(tile, maze), "Position out of bounds"
    if maze[tile[1]][tile[0]] == Tile.POWERUP:
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
    if (
        new_dir == Direction.LEFT
        and dir == Direction.RIGHT
        or new_dir == Direction.RIGHT
        and dir == Direction.LEFT
        or new_dir == Direction.UP
        and dir == Direction.DOWN
        or new_dir == Direction.DOWN
        and dir == Direction.UP
    ):
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


def get_squared_distance(tile1, tile2):
    return (tile1[0] - tile2[0]) ** 2 + (tile1[1] - tile2[1]) ** 2


def update_ghosts(pacman_state, ghost_states, maze):
    player_tile = pacman_state[0]
    dir_list = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
    for i in range(len(ghost_states)):
        tile = ghost_states[i][0]
        dir = ghost_states[i][1]
        best_dist = float("inf")
        best_dir = None
        best_tile = None
        for new_dir in dir_list:
            new_tile = move(tile, new_dir, maze)
            if not can_turn(dir, new_dir) or is_wall(new_tile, maze):
                continue
            dist = get_squared_distance(new_tile, player_tile)
            if dist < best_dist:
                best_dist = dist
                best_dir = new_dir
                best_tile = new_tile
        ghost_states[i] = (best_tile, best_dir)
    return ghost_states


def update_pacman(pacman_state, new_dir, maze):
    tile, dir = pacman_state
    if (
        new_dir
        and can_turn(dir, new_dir)
        and not is_wall(move(tile, new_dir, maze), maze)
    ):
        dir = new_dir
    new_tile = move(tile, dir, maze)
    if is_wall(new_tile, maze):
        return (tile, None)
    return (new_tile, dir)


def get_reward(state, maze):
    pacman_state = state[0]
    tile = pacman_state[0]
    if is_coin(tile, maze):
        maze[tile[1]][tile[0]] = Tile.EMPTY
        return 1
    if is_powerup(tile, maze):
        maze[tile[1]][tile[0]] = Tile.EMPTY
        return 5
    # todo: if is_ghost
    return 0


def action(state, new_dir, maze):
    """
    I am at tile, and I want to move in dir.
    """
    pacman_state = state[0]
    ghost_states = state[1]
    ghost_states = update_ghosts(pacman_state, ghost_states, maze)
    pacman_state = update_pacman(pacman_state, new_dir, maze)
    reward = get_reward(state, maze)

    return (pacman_state, ghost_states), reward


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
