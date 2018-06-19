import numpy as np
import gym
import gym.spaces
from loop_engine import Engine

class LoopEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)
        self.done = False
        
        self.actions = {0: self.engine.move_left,
                        1: self.engine.move_right,
                        2: self.engine.move_down,
                        3: self.engine.move_up,
                        4: self.engine.no_move}
                        
        self.action_space = gym.spaces.Discrete(5)
   
        self.path_xmin = 2
        self.path_xmax = 8
        self.path_ymin = 2
        self.path_ymax = 8

    def reset(self):
        self.engine.reset() 
        return np.array([self.engine.x,self.engine.y])

    def step(self,action):
        curr_state = self.engine.get_state()
        next_state = self.actions[action]()
        reward = self.get_reward(curr_state, action)
        return next_state, reward, self.done, {}

    def get_state(self):
        return self.engine.get_state()

    def get_reward(self,state, action):
        x = state[0]
        y = state[1]

        if x == self.path_xmax and action == 2 and (y <= self.path_ymax and y > self.path_ymin):
            return 0
        elif x == self.path_xmin and action == 3 and (y < self.path_ymax and y >= self.path_ymin):
            return 0
        elif y == self.path_ymax and action == 1 and (x < self.path_xmax and x >= self.path_xmin):
            return 0
        elif y == self.path_ymin and action == 0 and (x <= self.path_xmax and x > self.path_xmin):
            return 0
        else: 
            return -1

    def render(self, mode ='human'):
        return 0 
