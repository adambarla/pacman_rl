from enum import CONTINUOUS
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
from utils.constants import (
    GHOST_COLORS,
    PLAYER_PLAYING,
    REWARD_FOR_DEATH,
    REWARD_PER_KILL,
    SPEED_PER_SECOND,
    TICK_PER_SECOND,
)
from utils.general import maze_to_state
from utils.player import Player, Q_learning


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
    font = pg.font.SysFont("berkeleymonotrial", TILE_SIZE)

    player_playing = PLAYER_PLAYING
    if player_playing:
        player = Player()
        continuous = CONTINUOUS
    else:
        player = Q_learning()
        continuous = False

    running = True
    T = 100
    n = 0
    active_ghosts = 1
    while running:
        n += 1
        score = 0
        lives = 3
        maze = start_maze
        while lives > 0:
            t = 0
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
                maze_to_state(maze),
            )
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False

                screen.fill((0, 0, 0))
                draw_maze(screen, maze, offset=OFFSET)
                draw_movable(screen, pacman, maze, offset=OFFSET, continuous=continuous)
                for ghost in ghosts:
                    draw_movable(
                        screen, ghost, maze, offset=OFFSET, continuous=continuous
                    )

                screen.blit(
                    font.render(f"{score}", 1, "yellow"), (OFFSET * TILE_SIZE, 0)
                )
                screen.blit(
                    font.render(f"{lives}", 1, "red"), ((w - 1 + OFFSET) * TILE_SIZE, 0)
                )
                screen.blit(
                    font.render(f"{t//TICK_PER_SECOND}", 1, "white"),
                    ((w - 1 + OFFSET) * TILE_SIZE, (h + OFFSET) * TILE_SIZE),
                )
                screen.blit(
                    font.render(f"{int(clock.get_fps())}", 1, "white"),
                    (OFFSET * TILE_SIZE, (h + OFFSET) * TILE_SIZE),
                )

                pg.display.flip()
                if player_playing:
                    clock.tick(TICK_PER_SECOND)
                    new_distance = SPEED_PER_SECOND / TICK_PER_SECOND
                else:
                    clock.tick()
                    new_distance = 1
                distance += new_distance

                pacman.move(new_distance)
                for ghost in ghosts:
                    ghost.move(new_distance)

                # tick the game state based on speed
                if distance >= 1:
                    new_dir = player.get_action(state=state)
                    distance = 0
                    prev_state = state
                    state, reward = update(prev_state, new_dir, t)
                    if reward == REWARD_FOR_DEATH:
                        lives -= 1
                        break
                    score += reward
                    pacman_state, ghost_states, maze, phase = state
                    player.update(
                        state=prev_state,
                        action=new_dir,
                        reward=reward,
                        next_state=state,
                    )

                    pacman.set_state(pacman_state)
                    for i, ghost in enumerate(ghosts):
                        ghost.set_state(ghost_states[i])
                t += 1

    pg.quit()
