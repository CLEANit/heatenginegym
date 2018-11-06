import numpy as np
import gym
import gym.spaces
from cleangym.engine import Engine
from cleangym.heat_engine import HeatEngineEnv

class OttoEnv(HeatEngineEnv):
    def __init__(self, *args, **kwargs):
        super(OttoEnv, self).__init__(*args, **kwargs)

        self.actions = {0: self.engine.N_D,
                        1: self.engine.push_D,
                        2: self.engine.pull_D,
                        3: self.engine.N_Tc,
                        4: self.engine.N_Th}

        self.dV_actions = {0: self.engine.dVi,
                           1: self.engine.dVi / 10.0,
                           2: self.engine.dVi / 100.0,
                           3: self.engine.dVi / 1000.0,
                           4: self.engine.dVi / 10000.0}

        self.action_map = {
               'N_D':0,
               'push_D':1,
               'pull_D':2,
               'N_Tc':3,
               'N_Th':4,
             }
        self.Q = []
        self.W = []

        self.action_space = gym.spaces.Discrete(len(self.action_map) * len(self.dV_actions))
        self.observation_space = gym.spaces.Box(low=np.array([0,0]), high=np.array([1000.,1000.]),dtype=np.float32)

    def get_perfect_action_set(self, cycles=1):
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
