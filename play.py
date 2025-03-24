import pygame as pg
import numpy as np

from utils import (
    Direction,
    Movable,
    action,
    draw_movable,
    draw_maze,
    TILE_SIZE,
    MAZE,
    OFFSET,
)


def load_maze(maze):
    w = len(maze[0])
    h = len(maze)
    maze_array = np.zeros((h, w), dtype=int)
    start_pos = None
    ghost_spawn = None
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if maze[i][j] == "=" or maze[i][j] == "|" or maze[i][j] == "-":
                maze_array[i][j] = 1
            if maze[i][j] == ".":
                maze_array[i][j] = 2
            if maze[i][j] == "o":
                maze_array[i][j] = 3
            if maze[i][j] == "S":
                start_pos = (j, i)
            if maze[i][j] == "G":
                ghost_spawn = (j, i)
    assert start_pos is not None, "Start position not found"
    assert ghost_spawn is not None, "Ghost spawn position not found"
    assert maze_array[start_pos[1]][start_pos[0]] == 0, "Start position is not empty"
    assert maze_array[ghost_spawn[1]][ghost_spawn[0]] == 0, "Ghost spawn position is not empty"
    return maze_array, start_pos, ghost_spawn


if __name__ == "__main__":
    maze, start_pos, ghost_spawn = load_maze(MAZE)
    w = maze.shape[1]
    h = maze.shape[0]

    pg.init()
    screen = pg.display.set_mode(((w + 2*OFFSET) * TILE_SIZE, (h + 2* OFFSET) * TILE_SIZE))
    pg.display.set_caption("pacman")
    clock = pg.time.Clock()
    font = pg.font.SysFont("berkeleymonotrial", 30)

    speed = 5/1000 

    pacman = Movable((255, 255, 0), start_pos)
    ghosts = [Movable((255, 0, 0), ghost_spawn)]
    new_dir = None # acts as a buffer for the next direction, executed on the next intersection
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
        draw_movable(screen, pacman, maze, offset=OFFSET)
        for ghost in ghosts:
            draw_movable(screen, ghost, maze, offset=OFFSET)
        
        label = font.render(f"{score}", 1, 'white')
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