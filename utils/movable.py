from utils.constants import TILE_SIZE, Direction



class Movable:
    def __init__(self, color, pos, dir=None, size=TILE_SIZE//2):
        self.pos = pos
        self.dir = dir
        self.prev_pos = pos
        self.drawing_offset = (0.0, 0.0)
        self.color = color
        self.size = size
    
    def move(self, distance):
        if self.dir == Direction.LEFT:
            self.drawing_offset = (self.drawing_offset[0] - distance, self.drawing_offset[1])
        if self.dir == Direction.RIGHT:
            self.drawing_offset = (self.drawing_offset[0] + distance, self.drawing_offset[1])
        if self.dir == Direction.UP:
            self.drawing_offset = (self.drawing_offset[0], self.drawing_offset[1] - distance)
        if self.dir == Direction.DOWN:
            self.drawing_offset = (self.drawing_offset[0], self.drawing_offset[1] + distance)


    def set_state(self, state):
        self.prev_pos = self.pos
        self.pos = state[0]
        self.dir = state[1]
        self.drawing_offset = (0.0, 0.0)
    
    def get_state(self):
        return (self.pos, self.dir) 