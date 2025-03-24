import pygame as pg
from utils.constants import TILE_SIZE
from utils.general import is_coin, is_powerup, is_wall


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
                pg.draw.circle(
                    screen,
                    (255, 184, 174),
                    (x + TILE_SIZE // 2, y + TILE_SIZE // 2),
                    TILE_SIZE // 4,
                )
            elif is_coin((j, i), maze):
                pg.draw.circle(
                    screen,
                    (255, 184, 174),
                    (x + TILE_SIZE // 2, y + TILE_SIZE // 2),
                    TILE_SIZE // 8,
                )


def draw_movable(screen, movable, maze, offset=0, continuous=True):
    w = maze.shape[1]
    h = maze.shape[0]
    pos = (
        (movable.prev_pos[0] + offset) * TILE_SIZE,
        (movable.prev_pos[1] + offset) * TILE_SIZE,
    )
    if continuous:
        pos = (
            pos[0] + movable.drawing_offset[0] * TILE_SIZE,
            pos[1] + movable.drawing_offset[1] * TILE_SIZE,
        )
    pos = (pos[0] + movable.size, pos[1] + movable.size)
    pg.draw.circle(screen, movable.color, pos, movable.size)
    # draw aditional movable one board width away and one board height away
    if movable.prev_pos[0] == 0:
        pg.draw.circle(
            screen, movable.color, (pos[0] + w * TILE_SIZE, pos[1]), movable.size
        )
    if movable.prev_pos[1] == 0:
        pg.draw.circle(
            screen, movable.color, (pos[0], pos[1] + h * TILE_SIZE), movable.size
        )
    if movable.prev_pos[0] == w - 1:
        pg.draw.circle(
            screen, movable.color, (pos[0] - w * TILE_SIZE, pos[1]), movable.size
        )
    if movable.prev_pos[1] == h - 1:
        pg.draw.circle(
            screen, movable.color, (pos[0], pos[1] - h * TILE_SIZE), movable.size
        )
