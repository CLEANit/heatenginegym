import numpy as np
import gym
import gym.spaces
from cleangym.engine import Engine
import matplotlib.pyplot as plt
from cleangym.heat_engine import HeatEngineEnv

class StirlingEnv(HeatEngineEnv):
    def __init__(self, *args, **kwargs):
        super(StirlingEnv, self).__init__(*args, **kwargs)

        self.efficiency = (self.engine.Th - self.engine.Tc) / (self.engine.Th + (self.engine.Cv * (self.engine.Th - self.engine.Tc)) / (self.engine.N * self.engine.R * np.log(self.engine.Vmax / self.engine.Vmin)))

        self.actions = {0: self.engine.N_D,
                        1: self.engine.N_Tc,
                        2: self.engine.push_Tc,
                        3: self.engine.pull_Tc,
                        4: self.engine.N_Th,
                        5: self.engine.push_Th,
                        6: self.engine.pull_Th}

        self.dV_actions = {0: self.engine.dVi,
                           1: self.engine.dVi / 10.0,
                           2: self.engine.dVi / 100.0,
                           3: self.engine.dVi / 1000.0,
                           4: self.engine.dVi / 10000.0}

        self.action_map = {
               'N_D':0,
               'N_Tc':1,
               'push_Tc':2,
               'pull_Tc':3,
               'N_Th':4,
               'push_Th':5,
               'pull_Th':6
             }

        self.action_space = gym.spaces.Discrete(len(self.action_map) * len(self.dV_actions))
        self.observation_space = gym.spaces.Box(low=np.array([0,0]), high=np.array([1000.,1000.]),dtype=np.float32)

    def get_perfect_action_set(self, cycles=1):
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
