import pygame
import numpy as np

from utils import (
    Direction,
    update,
    TILE_SIZE,
)

from utils.general import is_wall, try_turning

class Tile:
    EMPTY = 0
    WALL = 1
    COIN = 2
    POWERUP = 3



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
    "      .   |      |   .      ",
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

def draw_maze(screen, maze):
    w = maze.shape[1]
    h = maze.shape[0]
    for i in range(h):
        for j in range(w):
            if is_wall((j, i), maze):
                pygame.draw.rect(screen, (33, 33, 255), (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_pacman(screen, pos):
    pos =tuple(p*TILE_SIZE + TILE_SIZE/2 for p in pos)
    pygame.draw.circle(screen, (255, 255, 0), pos, TILE_SIZE//2)
    

if __name__ == "__main__":

    maze, start_pos, ghost_spawn = load_maze(MAZE)
    w = maze.shape[1]
    h = maze.shape[0]

    pygame.init()
    screen = pygame.display.set_mode((w * TILE_SIZE, h * TILE_SIZE))
    pygame.display.set_caption("pacman")
    clock = pygame.time.Clock()

    speed = 5
    player_speed = 0.5

    pos = start_pos
    dir = None
    new_dir = None # acts as a buffer for the next direction, executed on the next intersection
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_maze(screen, maze)
        draw_pacman(screen, pos)

        pygame.display.flip()
        clock.tick(50)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            new_dir = Direction.LEFT
        if keys[pygame.K_RIGHT]:
            new_dir = Direction.RIGHT
        if keys[pygame.K_UP]:
            new_dir = Direction.UP
        if keys[pygame.K_DOWN]:
            new_dir = Direction.DOWN

        dir, new_dir = try_turning(pos, dir, new_dir, maze)
        pos, dir = update(pos, dir, maze)

    pygame.quit()