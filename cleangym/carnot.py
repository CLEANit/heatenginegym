import numpy as np
import gym
import gym.spaces
from engine import Engine




class CarnotEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)

        self.done = False

        self.actions = {0: self.engine.N_D,
                        1: self.engine.push_D,
                        2: self.engine.pull_D,
                        3: self.engine.N_Tc,
                        4: self.engine.push_Tc,
                        5: self.engine.pull_Tc,
                        6: self.engine.N_Th,
                        7: self.engine.push_Th,
                        8: self.engine.pull_Th}

        self.action_map = {
               'N_D':0,
               'push_D':1,
               'pull_D':2,
               'N_Tc':3,
               'push_Tc':4,
               'pull_Tc':5,
               'N_Th':6,
               'push_Th':7,
               'pull_Th':8
             }
        self.Q = []
        self.W = []

        self.action_space = gym.spaces.Discrete(9)

    def reset(self):
        self.engine.reset()
        self.Q = []
        self.W = []
        return np.array([self.engine.T, self.engine.V])

    def step(self, action):
        self.engine.T, self.engine.V, self.dW, self.dQ = self.actions[action]()
        self.Q.append(self.dQ)
        self.W.append(self.dW)
        try:
            r = float(np.array(self.W).sum() / np.array(self.Q).sum())
        except ZeroDivisionError:
            r = -1.0
        return np.array([self.engine.T, self.engine.V]), r, self.done, self.dQ



    def get_perfect_carnot_action_set(self, cycles=1):
        VA = self.engine.Vmin
        VD = VA * (self.engine.Th / self.engine.Tc)**(3./2.)
        VC = self.engine.Vmax
        VB = VC * (self.engine.Tc / self.engine.Th)**(3./2.)

        N1, N2, N3, N4 = [int( abs(VC-VD)/self.engine.dV),int( abs(VD-VA)/self.engine.dV),int( abs(VB-VA)/self.engine.dV),int( abs(VC-VB)/self.engine.dV)]
        actions = []
        for c in range(cycles):
            for i in range(N1):
                actions.append('push_Tc')
            for i in range(N2):
                actions.append('push_D')
            for i in range(N3):
                actions.append('pull_Th')
            for i in range(N4):
                actions.append('pull_D')

        self.engine.Pmax = self.engine.N * self.engine.R * self.engine.Th / VA
        self.engine.Pmin = self.engine.N * self.engine.R * self.engine.Tc / VC



        return actions

