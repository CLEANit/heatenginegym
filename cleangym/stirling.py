import numpy as np
import gym
import gym.spaces
from cleangym.engine import Engine




class StirlingEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)

        self.done = False

        self.efficiency = (self.engine.Th - self.engine.Tc) / (self.engine.Th + (self.engine.Cv * (self.engine.Th - self.engine.Tc)) / (self.engine.N * self.engine.R * np.log(self.engine.Vmax / self.engine.Vmin)))

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

    def get_perfect_stirling_action_set(self, cycles=1):
        VA = self.engine.Vmin
        VB = self.engine.Vmax
        N1 = int(abs(VB - VA)/self.engine.dV)
        N2 = 1
        N3 = int(abs(VA - VB)/self.engine.dV)
        N4 = 1
        actions = []
        for c in range(cycles):
            for i in range(N1):
                actions.append('push_Tc')
            for i in range(N2):
                actions.append('N_Th')
            for i in range(N3):
                actions.append('pull_Th')
            for i in range(N4):
                actions.append('N_Tc')

        return actions
