import pygame as pg
import numpy as np

from utils import (
    Direction,
    Movable,
    action,
    is_wall,
    is_coin,
    is_powerup,
    action,
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

def draw_maze(screen, maze, offset=0):
    w = maze.shape[1]
    h = maze.shape[0]
    for i in range(h):
        for j in range(w):
            x = (j + offset) * TILE_SIZE
            y = (i + offset) * TILE_SIZE
            if is_wall((j, i), maze):
                pg.draw.rect(screen, (33, 33, 255), (x, y, TILE_SIZE, TILE_SIZE))
            elif is_powerup((j, i), maze):
                pg.draw.circle(screen, (255, 184, 174), (x + TILE_SIZE//2, y + TILE_SIZE//2), TILE_SIZE//4)
            elif is_coin((j, i), maze):
                pg.draw.circle(screen, (255, 184, 174), (x + TILE_SIZE//2, y + TILE_SIZE//2), TILE_SIZE//8)

        
def draw_movable(screen, movable, maze, offset=0, continuous=False):
    w = maze.shape[1]
    h = maze.shape[0]
    pos = ((movable.prev_pos[0] + offset) * TILE_SIZE,  (movable.prev_pos[1] + offset) * TILE_SIZE )
    if not continuous:
        pos = (pos[0] + movable.drawing_offset[0] * TILE_SIZE, pos[1] + movable.drawing_offset[1] * TILE_SIZE)
    pos = (pos[0] + movable.size, pos[1] + movable.size)
    pg.draw.circle(screen, movable.color, pos, movable.size)
    # draw aditional movable one board width away and one board height away
    if movable.prev_pos[0] == 0:
        pg.draw.circle(screen, movable.color, (pos[0] + w * TILE_SIZE, pos[1]), movable.size)
    if movable.prev_pos[1] == 0:
        pg.draw.circle(screen, movable.color, (pos[0], pos[1] + h * TILE_SIZE), movable.size)
    if movable.prev_pos[0] == w - 1:
        pg.draw.circle(screen, movable.color, (pos[0] - w * TILE_SIZE, pos[1]), movable.size)
    if movable.prev_pos[1] == h - 1:
        pg.draw.circle(screen, movable.color, (pos[0], pos[1] - h * TILE_SIZE), movable.size)

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
        distance = speed * time
        pacman.move(distance)
        for ghost in ghosts:
            ghost.move(distance)
        

        if (abs(pacman.drawing_offset[0]) + abs(pacman.drawing_offset[1]) >= 1 
            or (pacman.dir is None and new_dir is not None)
            ):
            state = (pacman.get_state(), [g.get_state() for g in ghosts])
            (pacman_state, ghost_states), reward = action(state, new_dir, maze)

            pacman.set_state(pacman_state)
            for i, ghost in enumerate(ghosts):
                ghost.set_state(ghost_states[i])
            
            if pacman.dir == new_dir:
                new_dir = None
            score += reward
        

    pg.quit()