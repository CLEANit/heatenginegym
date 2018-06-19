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
   
    def reset(self):
        self.engine.reset() 
        return np.array([self.engine.x,self.engine.y])

    def step(self,action):
        curr_state = self.engine.get_state()
        next_state = self.actions[action]()
        reward = self.get_reward(curr_state, action)
        return next_state, reward, self.done

    def get_state(self):
        return self.engine.get_state()

    def get_reward(self, state, action):
        x = state[0]
        y = state[1]
        if x == self.engine.xmax and y!= self.engine.ymin and action == 2:
            return 0
        elif x == self.engine.xmin and y != self.engine.ymax and action == 3:
            return 0
        elif y == self.engine.ymax and x != self.engine.xmax and action == 1:
            return 0
        elif y == self.engine.ymin and x != self.engine.xmin and action == 0:
            return 0
        else: 
            return -1

    def render(self, mode ='human'):
        return 0 
