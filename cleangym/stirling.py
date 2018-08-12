import numpy as np
import gym
import gym.spaces
from engine import Engine




class StirlingEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)

        self.done = False

        self.actions = {0: self.engine.N_D,
                        1: self.engine.N_Tc,
                        2: self.engine.push_Tc,
                        3: self.engine.pull_Tc,
                        4: self.engine.N_Th,
                        5: self.engine.push_Th,
                        6: self.engine.pull_Th}

        self.action_map = {
               'N_D':0,
               'N_Tc':1,
               'push_Tc':2,
               'pull_Tc':3,
               'N_Th':4,
               'push_Th':5,
               'pull_Th':6
             }
        self.Q = []
        self.W = []

        self.action_space = gym.spaces.Discrete(7)

    def reset(self):
        self.engine.reset()
        self.Q = []
        self.W = []
        T = (self.engine.T - self.engine.Tmin) / (self.engine.Tmax - self.engine.Tmin)
        V = (self.engine.V - self.engine.Vmin) / (self.engine.Vmax - self.engine.Vmin)
        return np.array([T, V])
        #return np.array([self.engine.T, self.engine.V])

    def step(self, action):
        self.engine.T, self.engine.V, self.dW, self.dQ = self.actions[action]()
        self.Q.append(self.dQ)
        self.W.append(self.dW)
        try:
            r = float(np.array(self.W).sum()) / float(np.array(self.Q).sum())
        except ZeroDivisionError:
            r = -1.0
        T = (self.engine.T - self.engine.Tmin) / (self.engine.Tmax - self.engine.Tmin)
        V = (self.engine.V - self.engine.Vmin) / (self.engine.Vmax - self.engine.Vmin)
        return np.array([T, V]), r, self.done, np.array([self.engine.T, self.engine.V, self.engine.P])
        #return np.array([self.engine.T, self.engine.V]), r, self.done, self.engine.P

