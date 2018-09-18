import numpy as np
import gym
import gym.spaces
from cleangym.engine import Engine




class OttoEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)

        self.done = False

        self.actions = {0: self.engine.N_D,
                        1: self.engine.push_D,
                        2: self.engine.pull_D,
                        3: self.engine.N_Tc,
                        4: self.engine.N_Th}

        self.action_map = {
               'N_D':0,
               'push_D':1,
               'pull_D':2,
               'N_Tc':3,
               'N_Th':4,
             }
        self.Q = []
        self.W = []

        self.action_space = gym.spaces.Discrete(5)

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



    def get_perfect_otto_action_set(self, cycles=1):
        VA = self.engine.Vmin
        VB = self.engine.Vmax

        N1, N2, N3, N4 = [int( abs(VB-VA)/self.engine.dV),int(1),int( abs(VA-VB)/self.engine.dV),int(1)]
        actions = []
        for c in range(cycles):
            for i in range(N1):
                actions.append('push_D')
            for i in range(N2):
                actions.append('N_Th')
            for i in range(N3):
                actions.append('pull_D')
            for i in range(N4):
                actions.append('N_Tc')

        self.engine.Pmax = self.engine.N * self.engine.R * self.engine.Th / VA
        self.engine.Pmin = self.engine.N * self.engine.R * self.engine.Tc / VC



        return actions

