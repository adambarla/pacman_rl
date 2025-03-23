import pygame
import numpy as np

from utils import (
    Direction,
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
                pygame.draw.rect(screen, (33, 33, 255), (x, y, TILE_SIZE, TILE_SIZE))
            elif is_powerup((j, i), maze):
                pygame.draw.circle(screen, (255, 184, 174), (x + TILE_SIZE//2, y + TILE_SIZE//2), TILE_SIZE//4)
            elif is_coin((j, i), maze):
                pygame.draw.circle(screen, (255, 184, 174), (x + TILE_SIZE//2, y + TILE_SIZE//2), TILE_SIZE//8)

def draw_pacman(screen, boar_pos, drawing_offset, maze, offset=0):
    pos = ((boar_pos[0] + drawing_offset[0] + offset) * TILE_SIZE,(boar_pos[1] + drawing_offset[1] + offset) * TILE_SIZE )
    pos = (pos[0] + TILE_SIZE//2, pos[1] + TILE_SIZE//2)
    pygame.draw.circle(screen, (255, 255, 0), pos, TILE_SIZE//2)
    # draw aditional pacman one board width away and one board height away
    w = maze.shape[1]
    h = maze.shape[0]
    if boar_pos[0] == 0:
        pygame.draw.circle(screen, (255, 255, 0), (pos[0] + w * TILE_SIZE, pos[1]), TILE_SIZE//2)
    if boar_pos[1] == 0:
        pygame.draw.circle(screen, (255, 255, 0), (pos[0], pos[1] + h * TILE_SIZE), TILE_SIZE//2)
    if boar_pos[0] == w - 1:
        pygame.draw.circle(screen, (255, 255, 0), (pos[0] - w * TILE_SIZE, pos[1]), TILE_SIZE//2)
    if boar_pos[1] == h - 1:
        pygame.draw.circle(screen, (255, 255, 0), (pos[0], pos[1] - h * TILE_SIZE), TILE_SIZE//2)
    

if __name__ == "__main__":
    maze, start_pos, ghost_spawn = load_maze(MAZE)
    w = maze.shape[1]
    h = maze.shape[0]

    pygame.init()
    screen = pygame.display.set_mode(((w + 2*OFFSET) * TILE_SIZE, (h + 2* OFFSET) * TILE_SIZE))
    pygame.display.set_caption("pacman")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("berkeleymonotrial", 30)

    speed = 5/1000 

    board_pos = start_pos
    prev_board_pos = start_pos
    drawing_offset = (0.0,0.0)
    dir = None
    new_dir = None # acts as a buffer for the next direction, executed on the next intersection
    running = True
    score = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_maze(screen, maze, offset=OFFSET)
        draw_pacman(screen, prev_board_pos, drawing_offset, maze, offset=OFFSET)
        label = font.render(f"{score}", 1, 'white')
        screen.blit(label, (0, 0))

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

        time = clock.get_time() 
        distance = speed * time
        if dir == Direction.LEFT:
            drawing_offset = (drawing_offset[0] - distance, drawing_offset[1])
        if dir == Direction.RIGHT:
            drawing_offset = (drawing_offset[0] + distance, drawing_offset[1])
        if dir == Direction.UP:
            drawing_offset = (drawing_offset[0], drawing_offset[1] - distance)
        if dir == Direction.DOWN:
            drawing_offset = (drawing_offset[0], drawing_offset[1] + distance)

        if abs(drawing_offset[0]) + abs(drawing_offset[1]) >= 1 or dir is None:
            drawing_offset = (0.0, 0.0)
            prev_board_pos = board_pos
            board_pos, dir, reward = action(board_pos, dir, new_dir, maze)
            if dir == new_dir:
                new_dir = None
            score += reward
        

    pygame.quit()