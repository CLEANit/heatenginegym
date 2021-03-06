import numpy as np
import gym
import gym.spaces
from heatenginegym.engine import Engine




class CarnotEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)

        self.done = False

        self.actions = {0: self.engine.push_D,
                        1: self.engine.pull_D,
                        2: self.engine.push_Tc,
                        3: self.engine.pull_Th}

        self.action_map = {
               'push_D':0,
               'pull_D':1,
               'push_Tc':2,
               'pull_Th':3
             }
        self.Q = []
        self.W = []

        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=np.array([self.engine.Tmin, self.engine.Vmin]), high=np.array([self.engine.Tmax, self.engine.Vmax]),dtype=np.float32)


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
            r = float(np.array(self.W).sum()) / float(np.array(self.Q).sum())
        except ZeroDivisionError:
            r = -1.1
        T = (self.engine.T - self.engine.Tmin) / (self.engine.Tmax - self.engine.Tmin)
        V = (self.engine.V - self.engine.Vmin) / (self.engine.Vmax - self.engine.Vmin)
        return np.array([self.engine.T, self.engine.V]), r, self.done, self.engine.P



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

