from utils.constants import TILE_SIZE, Direction


class Movable:
    def __init__(
        self,
        color,
        spawn_pos,
        home_pos=None,
        active=True,
        dir=None,
        size=TILE_SIZE // 2,
    ):
        self.color = color
        self.home_pos = home_pos if home_pos is not None else spawn_pos
        self.pos = spawn_pos
        self.active = active
        self.dir = dir
        self.prev_pos = self.pos
        self.drawing_offset = (0.0, 0.0)
        self.size = size

    def move(self, distance):
        if self.dir == Direction.LEFT:
            self.drawing_offset = (
                self.drawing_offset[0] - distance,
                self.drawing_offset[1],
            )
        if self.dir == Direction.RIGHT:
            self.drawing_offset = (
                self.drawing_offset[0] + distance,
                self.drawing_offset[1],
            )
        if self.dir == Direction.UP:
            self.drawing_offset = (
                self.drawing_offset[0],
                self.drawing_offset[1] - distance,
            )
        if self.dir == Direction.DOWN:
            self.drawing_offset = (
                self.drawing_offset[0],
                self.drawing_offset[1] + distance,
            )

    def set_state(self, state):
        self.prev_pos = self.pos
        self.pos = state[0]
        self.dir = state[1]
        self.active = state[2]
        self.drawing_offset = (0.0, 0.0)
        return

    def get_state(self):
        state = (self.pos, self.dir, self.active)
        return state
