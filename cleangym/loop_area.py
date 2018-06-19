import numpy as np
import gym
import gym.spaces
from loop_engine import Engine

def segments(p):
    return zip(p, p[1:] + [p[0]])

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
        

        self.steps = []


    def reset(self):
        self.engine.reset() 
        state = self.get_state()
        self.steps.append(list(state))
        return np.array(state)

    def step(self,action):
        curr_state = self.engine.get_state()
        next_state = self.actions[action]()
        reward = self.get_reward(curr_state, action)
        return next_state, reward, self.done, {}

    def get_state(self):
        return self.engine.get_state()

    def overlap(self,points,p):
        n = len(points)
        if (p in points):
            i = points.index(p)
            return points[0:i+1], points[i:]
        else:
            return points, []

    def calc_area(self,points):
        return 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0,y0), (x1,y1)) in segments(points)))
   
    def get_reward(self,state, action):
        state = list(state)
        a,b = self.overlap(self.steps, state)
        self.steps.append(state)
        if len(b) != 0:
            b.append(state)
            self.steps = a
            area = self.calc_area(b)
            if area != 0:
                return area 
            else:
                return - 1
        else: 
            return -1

    def render(self, mode ='human'):
       return 0 
