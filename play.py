import pygame as pg
import numpy as np

from utils import (
    Direction,
    Movable,
    action,
    draw_movable,
    draw_maze,
    load_maze,
    TILE_SIZE,
    MAZE,
    OFFSET,
)

CONTINUOUS = True


if __name__ == "__main__":
    maze, start_pos, ghost_spawn = load_maze(MAZE)
    w = maze.shape[1]
    h = maze.shape[0]

    pg.init()
    screen = pg.display.set_mode(
        ((w + 2 * OFFSET) * TILE_SIZE, (h + 2 * OFFSET) * TILE_SIZE)
    )
    pg.display.set_caption("pacman")
    clock = pg.time.Clock()
    font = pg.font.SysFont("berkeleymonotrial", 30)

    speed = 5 / 1000

    pacman = Movable((255, 255, 0), start_pos)
    ghosts = [Movable((255, 0, 0), ghost_spawn)]
    new_dir = None  # acts as a buffer for the next direction, executed on the next intersection
    running = True
    score = 0
    distance = 0
    state = (pacman.get_state(), [g.get_state() for g in ghosts])
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_maze(screen, maze, offset=OFFSET)
        draw_movable(screen, pacman, maze, offset=OFFSET, continuous=CONTINUOUS)
        for ghost in ghosts:
            draw_movable(screen, ghost, maze, offset=OFFSET, continuous=CONTINUOUS)

        label = font.render(f"{score}", 1, "white")
        screen.blit(label, (0, 0))

        pg.display.flip()
        clock.tick(50)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            new_dir = Direction.LEFT
        if keys[pg.K_RIGHT]:
            new_dir = Direction.RIGHT
        if keys[pg.K_UP]:
            new_dir = Direction.UP
        if keys[pg.K_DOWN]:
            new_dir = Direction.DOWN

        time = clock.get_time()
        new_distance = speed * time
        distance += new_distance
        pacman.move(new_distance)
        for ghost in ghosts:
            ghost.move(new_distance)

        if dir is None:
            dir = new_dir
            new_dir = None

        if distance >= 1:
            distance = 0
            state = (pacman.get_state(), [g.get_state() for g in ghosts])
            (pacman_state, ghost_states), reward = action(state, new_dir, maze)

            pacman.set_state(pacman_state)
            for i, ghost in enumerate(ghosts):
                ghost.set_state(ghost_states[i])

            if pacman.dir == new_dir or pacman.dir is None:
                new_dir = None
            score += reward

    pg.quit()
