import gym
from gym import error, spaces, utils, logger
from gym.utils import seeding

import numpy as np
import math
from matplotlib import pyplot as plt

class Engine(object):
    def __init__(self, Tinit=300., Vinit=0.001):
        
        self.N = 1.0/22.4 # because 1 mole occupies 22.4 L at STP, number of moles of gas
        self.c = 5.0/3.0  # type of gas 
        self.R = 8.3144598 # units of J K−1 mol−1
        
        self.P_high_threshold = 1e7     #piston explodes at this pressure
        self.V_low_threshold = 1e-6     #basically zero, but not zero
        self.V_high_threshold = 1./1000. #[m^3]
        self.T_low_threshold = 1e-6     #absolute zero
        self.T_high_threshold = 1000.0  #Meltdown
        
        self.Tinit = Tinit
        self.Vinit = Vinit

        # we initialize the state of the world with _reset() method 
        self.T = Tinit  # temperature of gas 
        self.V = Vinit  # volume of gas 
        self.__state_update__()
        
    def __state_update__(self):
        '''
        Updates the state of the engine environment.
        '''
        self.P = self.N*self.T*self.R / self.V
        self.state = [self.T, self.V]
        
class CylinderEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, T_c=300., T_h=500., dV=0.1/1000.):
        # initialize "physics" of the world
        self.engine = Engine()
        self.T_c = T_c # temperature of the cold reservoir ~ room temperature
        self.T_h = T_h # temperature of the hot reservoir
        self.dV = dV
        self.action_space = spaces.Discrete(9)

    def get_state(self):
        self.state = [ self.engine.T, self.engine.V ]
        return self.state
        
        
    def _step(self, action):
        '''
        Performs an action from the list of available actions 
        (usually it is sampled from self.action_space)
        
        Modifies the state of the cylinder.
        
        Returns: 4-tuple: (new state as np.array, 
                           work done per this step, 
                           done (boolean), which is True if the action taken was not allowed,
                           dictionary with one entry, heat from the hot reservoir used during this step)
        '''
        actions = ["push_Tc", "push_Th", "push_N", 
                   "pull_Tc", "pull_Th", "pull_N", 
                   "N_Tc", "N_Th", "N_N"]
        
        T_old, V_old = self.get_state()
        done = False
        dQ = 0.
        dW = 0.
        
        if actions[action] == "push_Tc":
            self.engine.T = self.T_c
            self.engine.V = V_old - self.dV
            if self.engine.V > 0:
                dW = self.engine.N*self.engine.R*self.engine.T * math.log(self.engine.V/V_old)
                dQ = 0 
            
        elif actions[action] == "push_Th":
            self.engine.T = self.T_h
            self.engine.V = V_old - self.dV
            if self.engine.V > 0:
                dW = self.engine.N*self.engine.R*self.engine.T *math.log(self.engine.V/V_old)
                dQ = 0 
        
        elif actions[action] == "push_N":
            self.engine.V = V_old - self.dV 
            if self.engine.V > 0:
                self.engine.T = T_old * math.pow(V_old/self.engine.V, 2.0/3.0)

                dW = -3.0/2.0*self.engine.N*self.engine.R*(self.engine.T - T_old)
                dQ = 0 
            
        elif actions[action] == "pull_Tc":
            
            self.engine.T = self.T_c
            self.engine.V = V_old + self.dV

            dW = self.engine.N*self.engine.R*self.engine.T *math.log(self.engine.V/V_old)
            dQ = 0 
            
        elif actions[action] == "pull_Th":
            self.engine.T = self.T_h
            self.engine.V = V_old + self.dV
            
            dW = self.engine.N*self.engine.R*self.engine.T *math.log(self.engine.V/V_old)
            dQ = dW 
            
        elif actions[action] == "pull_N":
           
            self.engine.V = V_old + self.dV
            self.engine.T = self.engine.T * math.pow(V_old/self.engine.V, 2.0/3.0)
            
            dW = -3.0/2.0*self.engine.N*self.engine.R*(self.engine.T - T_old)
            dQ = 0 
            
        elif actions[action] == "N_Tc":
            self.engine.T = self.T_c
            self.engine.V = V_old
            
            dW = 0
            dQ = 0 
            
        elif actions[action] == "N_Th": 
            self.engine.T = self.T_h
            self.engine.V = V_old
           
            dW = 0 
            dQ = 0
            
        elif actions[action] == "N_N":
            dW = 0 
            dQ = 0
      
        if  (   self.engine.T < self.engine.T_low_threshold \
             or self.engine.T > self.engine.T_high_threshold \
             or self.engine.P > self.engine.P_high_threshold \
             or self.engine.V < self.engine.V_low_threshold \
             or self.engine.V > self.engine.V_high_threshold    ):
            self.engine.T = T_old
            self.engine.V = V_old
            reward = 0.0 
        else:
            reward = dW
            
        self.engine.__state_update__()

        
        return np.array(self.get_state()), reward, False, {'d_heat': dQ}   

    def _reset(self):
        '''
        Resets the cylinder environment to its initial state.
        '''
       # T = np.random.rand()*200 + 300 
       # V = np.random.rand() * 0.0009 + 0.0001
       # self.__state_update__(T, V)
        self.engine.T = self.engine.Tinit
        self.engine.V = self.engine.Vinit
        self.engine.__state_update__()
        return np.array(self.get_state())
    
    def _render(self, mode='human', close=False):
        return