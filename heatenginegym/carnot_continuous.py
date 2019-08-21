import numpy as np
import gym
import gym.spaces
from heatenginegym.engine import Engine
from heatenginegym.heat_engine_continuous import HeatEngineEnv

class CarnotEnv(HeatEngineEnv):
    def __init__(self, *args, **kwargs):
        super(CarnotEnv, self).__init__(*args, **kwargs)

        self.efficiency = (self.engine.Th - self.engine.Tc) / self.engine.Th

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

        self.action_space = gym.spaces.Box(np.array([0, 0]), np.array([len(self.actions) - 1, self.engine.Vmax - self.engine.Vmin]))
        self.observation_space = gym.spaces.Box(low=np.array([self.engine.Tmin, self.engine.Vmin]), high=np.array([self.engine.Tmax, self.engine.Vmax]),dtype=np.float32)

    def get_perfect_action_set(self, cycles=1):
        VA = self.engine.Vmin
        VD = VA * (self.engine.Th / self.engine.Tc)**(3./2.)
        VC = self.engine.Vmax
        VB = VC * (self.engine.Tc / self.engine.Th)**(3./2.)

        actions = []
        for c in range(cycles):
            actions.append(['push_Tc', (VC-VD)])
            actions.append(['push_D', (VD-VA)])
            actions.append(['N_Th', 0.0])
            actions.append(['pull_Th', (VB-VA)])
            actions.append(['pull_D', (VC-VB)])
            actions.append(['N_Tc', 0.0])

        self.engine.Pmax = self.engine.N * self.engine.R * self.engine.Th / VA
        self.engine.Pmin = self.engine.N * self.engine.R * self.engine.Tc / VC

        return actions

