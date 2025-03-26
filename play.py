import random
import pygame as pg

from utils import (
    Direction,
    Movable,
    update,
    draw_movable,
    draw_maze,
    load_maze,
    TILE_SIZE,
    MAZE,
    OFFSET,
)
from utils.constants import ACTIONS, GHOST_COLORS
from utils.general import maze_to_state

CONTINUOUS = True


def get_action(**kwargs):
    new_dir = None
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        new_dir = Direction.LEFT
    if keys[pg.K_RIGHT]:
        new_dir = Direction.RIGHT
    if keys[pg.K_UP]:
        new_dir = Direction.UP
    if keys[pg.K_DOWN]:
        new_dir = Direction.DOWN
    return new_dir


if __name__ == "__main__":

    pg.init()
    start_maze, start_pos, ghost_spawn, ghost_dens = load_maze(MAZE)
    h = len(start_maze)
    w = len(start_maze[0])
    screen = pg.display.set_mode(
        ((w + 2 * OFFSET) * TILE_SIZE, (h + 2 * OFFSET) * TILE_SIZE)
    )

    pg.display.set_caption("pacman")
    clock = pg.time.Clock()
    font = pg.font.SysFont("berkeleymonotrial", 30)

    speed = 5 / 1000

    running = True
    Q = {}
    T = 100
    n = 0
    active_ghosts = 1
    while running:
        n += 1
        score = 0
        distance = 0
        pacman = Movable((255, 255, 0), start_pos)
        ghosts = [
            Movable(
                GHOST_COLORS[i],
                ghost_spawn,
                ghost_dens[i],
                active=False,
                size=TILE_SIZE // 2,
            )
            for i in range(4)
        ]
        state = (
            pacman.get_state(),
            (tuple([g.get_state() for g in ghosts])),
            maze_to_state(start_maze),
        )
        maze = start_maze
        new_dir = None  # acts as a buffer for the next direction, executed on the next intersection
        t = 0
        T_episode = T + n * 10
        continuous = False
        while t < T_episode:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            draw_maze(screen, maze, offset=OFFSET)
            draw_movable(screen, pacman, maze, offset=OFFSET, continuous=continuous)
            for ghost in ghosts:
                draw_movable(screen, ghost, maze, offset=OFFSET, continuous=continuous)

            label = font.render(f"{score}", 1, "white")
            screen.blit(label, (0, 0))

            pg.display.flip()
            clock.tick(50)

            time = clock.get_time()
            new_distance = speed * time
            distance += new_distance
            pacman.move(new_distance)
            for ghost in ghosts:
                ghost.move(new_distance)

            def get_action(Q, state):
                if state not in Q:
                    Q[state] = {}
                for action in ACTIONS:
                    if action not in Q[state]:
                        Q[state][action] = 0
                best_action = None
                best_value = float("-inf")
                for action in Q[state]:
                    if Q[state][action] > best_value:
                        best_value = Q[state][action]
                        best_action = action
                if best_action is None:
                    return random.choice(ACTIONS)
                return best_action

            def update_Q(Q, state, action, reward, next_state, lr=0.1, gamma=0.9):
                if next_state not in Q:
                    Q[next_state] = {}
                if state not in Q:
                    Q[state] = {}
                if action not in Q[next_state]:
                    Q[next_state][action] = 0
                if action not in Q[state]:
                    Q[state][action] = 0
                Q[state][action] += lr * (
                    reward + gamma * max(Q[next_state].values()) - Q[state][action]
                )

            if dir is None:
                dir = new_dir
                new_dir = None

            if distance >= 1 or True:
                new_action = get_action(Q, state)
                if new_action is not None:
                    new_dir = new_action
                distance = 0
                prev_state = state
                state, reward = update(prev_state, new_dir, t)
                pacman_state, ghost_states, maze = state
                update_Q(Q, prev_state, new_dir, reward, state)
                t += 1
                # print(Q)

                pacman.set_state(pacman_state)
                for i, ghost in enumerate(ghosts):
                    ghost.set_state(ghost_states[i])

                if pacman.dir == new_dir or pacman.dir is None:
                    new_dir = None
                score += reward

    pg.quit()
