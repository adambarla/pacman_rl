import random
import pygame as pg
from utils.constants import ACTIONS, Direction


class Player:
    def __init__(self, **kwargs):
        self.new_dir = None
        pass

    def get_action(self, **kwargs):
        new_dir = self.new_dir
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            new_dir = Direction.LEFT
        if keys[pg.K_RIGHT]:
            new_dir = Direction.RIGHT
        if keys[pg.K_UP]:
            new_dir = Direction.UP
        if keys[pg.K_DOWN]:
            new_dir = Direction.DOWN
        self.new_dir = new_dir
        return new_dir

    def update(self, **kwargs):
        pass


class Q_learning:
    def __init__(self, lr=0.1, gamma=0.9, **kwargs):
        self.Q = {}
        self.lr = lr
        self.gamma = gamma

    def get_action(self, state, **kwargs):
        if state not in self.Q:
            self.Q[state] = {}
        for action in ACTIONS:
            if action not in self.Q[state]:
                self.Q[state][action] = 0
        best_action = None
        best_value = float("-inf")
        for action in self.Q[state]:
            if self.Q[state][action] > best_value:
                best_value = self.Q[state][action]
                best_action = action
        if best_action is None:
            return random.choice(ACTIONS)
        return best_action

    def update(self, state, action, reward, next_state, **kwargs):
        if next_state not in self.Q:
            self.Q[next_state] = {}
        if state not in self.Q:
            self.Q[state] = {}
        if action not in self.Q[next_state]:
            self.Q[next_state][action] = 0
        if action not in self.Q[state]:
            self.Q[state][action] = 0
        self.Q[state][action] += self.lr * (
            reward
            + self.gamma * max(self.Q[next_state].values())
            - self.Q[state][action]
        )
