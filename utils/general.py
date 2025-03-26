from utils.constants import (
    ACTIONS,
    CHASE_SECONDS,
    NEW_GHOST_WAIT,
    REWARD_FOR_DEATH,
    REWARD_PER_COIN,
    REWARD_PER_KILL,
    REWARD_PER_POWERUP,
    SCATTER_SECONDS,
    TICK_PER_SECOND,
    Direction,
    Phase,
    Tile,
)
import numpy as np


def load_maze(maze):
    w = len(maze[0])
    h = len(maze)
    maze_array = np.zeros((h, w), dtype=int)
    start_pos = None
    ghost_spawn = None
    ghost_dens = []
    for i, row in enumerate(maze):
        for j, tile in enumerate(row):
            if tile == "=" or tile == "|" or tile == "-":
                maze_array[i][j] = 1
            elif tile == ".":
                maze_array[i][j] = 2
            elif tile == "o":
                maze_array[i][j] = 3
            elif tile == "S":
                start_pos = (j, i)
            elif tile == "G":
                ghost_spawn = (j, i)
            elif tile == "D":
                ghost_dens.append((j, i))
    assert start_pos is not None, "Start position not found"
    assert ghost_spawn is not None, "Ghost spawn position not found"
    assert maze_array[start_pos[1]][start_pos[0]] == 0, "Start position is not empty"
    assert (
        maze_array[ghost_spawn[1]][ghost_spawn[0]] == 0
    ), "Ghost spawn position is not empty"
    if len(ghost_dens) == 0:
        ghost_dens = [ghost_spawn]
    return maze_to_state(maze_array), start_pos, ghost_spawn, ghost_dens


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


def is_ghost(tile, ghost_possitions):
    for g in ghost_possitions:
        if g[0] == tile:
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


def move(tile, dir, maze, distance=1):
    if not dir:
        return tile
    if dir == Direction.LEFT:
        new_pos = (tile[0] - distance, tile[1])
    if dir == Direction.RIGHT:
        new_pos = (tile[0] + distance, tile[1])
    if dir == Direction.UP:
        new_pos = (tile[0], tile[1] - distance)
    if dir == Direction.DOWN:
        new_pos = (tile[0], tile[1] + distance)
    new_pos = teleport(new_pos, maze)
    return new_pos


def get_squared_distance(tile1, tile2):
    return (tile1[0] - tile2[0]) ** 2 + (tile1[1] - tile2[1]) ** 2


def get_ghost_target(
    pacman_tile,
    pacman_dir,
    ghost_tiles,
    maze,
    ghost_index,
    phase=0,
):
    scatter_targets = [
        (0, 0),
        (len(maze[0]) - 1, 0),
        (0, len(maze) - 1),
        (len(maze[0]) - 1, len(maze) - 1),
    ]
    if phase == Phase.SCATTER:
        return scatter_targets[ghost_index]

    if ghost_index == 0:  # blinky
        return pacman_tile
    if ghost_index == 1:  # pinky
        return move(pacman_tile, pacman_dir, maze, 4)
    if ghost_index == 2:  # inky
        interm_tile = move(pacman_tile, pacman_dir, maze, 2)
        # rotate vector from interm to blinky by 180 degrees
        blinky_tile = ghost_tiles[0]
        return (
            interm_tile[0] + (interm_tile[0] - blinky_tile[0]),
            interm_tile[1] + (interm_tile[1] - blinky_tile[1]),
        )
    if ghost_index == 3:  # clyde
        dist = get_squared_distance(pacman_tile, ghost_tiles[3])
        if dist < 64:
            return scatter_targets[3]
        return pacman_tile

    # todo: add phases


def find_best_dir(tile, dir, target, maze):
    best_dist = float("inf")
    best_dir = None
    best_tile = None
    for new_dir in ACTIONS:
        new_tile = move(tile, new_dir, maze)
        if not can_turn(dir, new_dir) or is_wall(new_tile, maze):
            continue
        dist = get_squared_distance(new_tile, target)
        if dist < best_dist:
            best_dist = dist
            best_dir = new_dir
            best_tile = new_tile
    return best_tile, best_dir


def update_ghosts(pacman_state, ghost_states, maze, time, phase):
    ghost_states = list(ghost_states)
    pacman_tile = pacman_state[0]
    pacman_dir = pacman_state[1]
    ghost_tiles = [g[0] for g in ghost_states]
    for i in range(len(ghost_states)):
        dir = ghost_states[i][1]
        active = time // TICK_PER_SECOND // NEW_GHOST_WAIT + 1 > i
        if not active:
            continue
        target = get_ghost_target(pacman_tile, pacman_dir, ghost_tiles, maze, i, phase)
        best_tile, best_dir = find_best_dir(ghost_tiles[i], dir, target, maze)

        ghost_states[i] = (best_tile, best_dir, active)
    return tuple(ghost_states)


def update_pacman(pacman_state, new_dir, maze):
    tile = pacman_state[0]
    dir = pacman_state[1]
    if (
        new_dir
        and can_turn(dir, new_dir)
        and not is_wall(move(tile, new_dir, maze), maze)
    ):
        dir = new_dir
    new_tile = move(tile, dir, maze)
    if is_wall(new_tile, maze):
        return (tile, None, True)
    return (new_tile, dir, True)


def get_reward(state, maze, phase):
    pacman_state = state[0]
    tile = pacman_state[0]
    if is_ghost(tile, state[1]) and phase != Phase.FRIGHTENED:
        return REWARD_FOR_DEATH
    reward = 0
    if is_coin(tile, maze):
        maze[tile[1]][tile[0]] = Tile.EMPTY
        reward += REWARD_PER_COIN
    if is_powerup(tile, maze):
        maze[tile[1]][tile[0]] = Tile.EMPTY
        reward += REWARD_PER_POWERUP
    if is_ghost(tile, state[1]) and phase == Phase.FRIGHTENED:
        reward += REWARD_PER_KILL
    return reward


def maze_to_state(maze):
    state = []
    for i in range(len(maze)):
        state.append(tuple(maze[i]))
    return tuple(state)


def state_to_maze(state):
    maze = np.zeros((len(state), len(state[0])), dtype=int)
    for i in range(len(state)):
        for j in range(len(state[i])):
            maze[i][j] = state[i][j]
    return maze


def get_phase(time):
    is_scatter = (time // TICK_PER_SECOND) % (
        CHASE_SECONDS + SCATTER_SECONDS
    ) < SCATTER_SECONDS
    if is_scatter:
        return Phase.SCATTER
    else:
        return Phase.CHASE


def update(state, new_dir, time):
    """
    I am at tile, and I want to move in dir.
    """
    pacman_state = state[0]
    ghost_states = state[1]
    maze = state_to_maze(state[2])
    phase = get_phase(time)
    ghost_states = update_ghosts(pacman_state, ghost_states, maze, time, phase)
    pacman_state = update_pacman(pacman_state, new_dir, maze)
    reward = get_reward(state, maze, phase)

    return (pacman_state, ghost_states, maze_to_state(maze), phase), reward


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
