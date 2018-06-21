import numpy as np
import gym
import gym.spaces
from chemgrid import ChemGrid

class ChemWorldEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.ChemGrid = ChemGrid(*args, **kwargs)
        self.done = False
        self.product = 0
        self.goal = len(self.ChemGrid.recipes)

        self.actions = {0: self.ChemGrid.move_N,
                        1: self.ChemGrid.move_Up,
                        2: self.ChemGrid.move_Down,
                        3: self.ChemGrid.move_Left,
                        4: self.ChemGrid.move_Right,
                        5: self.ChemGrid.get_Truth}

        self.action_map = {
               'move_N':0,
               'move_Up':1,
               'move_Down':2,
               'move_Left':3,
               'move_Right':4,
               'get_Truth':5}

        self.action_space = gym.spaces.Discrete(6 + self.ChemGrid.sizeX + self.ChemGrid.sizeY)

    def reset(self):
        self.ChemGrid.reset()
        self.product = 0
        return self.ChemGrid.state

    def step(self, actions):
        action = actions[0]
        X_pos = actions[1]
        Y_pos = actions[2]
        self.actions[action](X_pos, Y_pos)
        product = self.ChemGrid.species[-1]
        r = product - self.product
        if action == 5:
            r -= self.ChemGrid.recipes[self.goal - 1][-1]
            r = np.max([r, 0.0])

        self.product = product
        _ = self.ChemGrid.species

        return self.ChemGrid.state, r, self.done, _
