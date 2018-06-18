import numpy as np
import gym
import gym.spaces
from gridobjects import GridObjects
import matplotlib.pyplot as plt

class GridWorldEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.GridObjects = GridObjects(*args, **kwargs)
        self.count = 0
        self.done = False
        self.rendering = False

        self.actions = {0: self.GridObjects.move_N,
                        1: self.GridObjects.move_A_Up,
                        2: self.GridObjects.move_A_Down,
                        3: self.GridObjects.move_A_Left,
                        4: self.GridObjects.move_A_Right,
                        5: self.GridObjects.move_B_Up,
                        6: self.GridObjects.move_B_Down,
                        7: self.GridObjects.move_B_Left,
                        8: self.GridObjects.move_B_Right,
                        9: self.GridObjects.move_A_Up_B_Up,
                        10: self.GridObjects.move_A_Up_B_Down,
                        11: self.GridObjects.move_A_Up_B_Left,
                        12: self.GridObjects.move_A_Up_B_Right,
                        13: self.GridObjects.move_A_Down_B_Up,
                        14: self.GridObjects.move_A_Down_B_Down,
                        15: self.GridObjects.move_A_Down_B_Left,
                        16: self.GridObjects.move_A_Down_B_Right,
                        17: self.GridObjects.move_A_Left_B_Up,
                        18: self.GridObjects.move_A_Left_B_Down,
                        19: self.GridObjects.move_A_Left_B_Left,
                        20: self.GridObjects.move_A_Left_B_Right,
                        21: self.GridObjects.move_A_Right_B_Up,
                        22: self.GridObjects.move_A_Right_B_Right,
                        23: self.GridObjects.move_A_Right_B_Left,
                        24: self.GridObjects.move_A_Right_B_Right}

        self.action_map = {
               'move_N':0,
               'move_A_Up':1,
               'move_A_Down':2,
               'move_A_Left':3,
               'move_A_Right':4,
               'move_B_Up':5,
               'move_B_Down':6,
               'move_B_Left':7,
               'move_B_Right':8,
               'move_A_Up_B_Up':9,
               'move_A_Up_B_Down':10,
               'move_A_Up_B_Left':11,
               'move_A_Up_B_Right':12,
               'move_A_Down_B_Up':13,
               'move_A_Down_B_Down':14,
               'move_A_Down_B_Left':15,
               'move_A_Down_B_Right':16,
               'move_A_Left_B_Up':17,
               'move_A_Left_B_Down':18,
               'move_A_Left_B_Left':19,
               'move_A_Left_B_Right':20,
               'move_A_Right_B_Up':21,
               'move_A_Right_B_Right':22,
               'move_A_Right_B_Left':23,
               'move_A_Right_B_Right':24,
            }

        self.action_space = gym.spaces.Discrete(25)

    def reset(self):
        self.GridObjects.reset()
        self.count = 0
        return self.GridObjects.state

    def step(self, action):
        self.actions[action]()
        if self.GridObjects.heroA_X == self.GridObjects.heroB_X and self.GridObjects.heroA_Y == self.GridObjects.heroB_Y:
            if self.count == 0:
                r = 1.0
                self.count += 1

            elif self.count == 5:
                r = 5.0
                self.reset()

            else:
                r = 0.0
                self.count += 1

        elif self.count != 0:
            r = -1.0

        else:
            r = 0.0

        _ = np.array([[self.GridObjects.heroA_X, self.GridObjects.heroA_Y], [self.GridObjects.heroB_X, self.GridObjects.heroB_Y]])

        return self.GridObjects.state, r, self.done, _

    def render(self, mode='human'):
        if not self.rendering:
            plt.ion()
            plt.axis('off')
            rendering = True

        else:
            plt.imshow(self.GridObjects.state)
