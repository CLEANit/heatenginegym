import gym
from gym import error, spaces, utils, logger
from gym.utils import seeding

import numpy as np
import math
from matplotlib import pyplot as plt

class EasyCylinderEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # initialize "physics" of the world
        
        self.N = 1.0/22.4 # because 1 mole occupies 22.4 L at STP, number of moles of gas
        self.c = 5.0/3.0  # type of gas 
        self.R = 8.3144598 # units of J K−1 mol−1
        
        self.P_low_threshold = 0.0 # MPa
        self.P_high_threshold = 10000000.0 # 10 MPa
        self.V_low_threshold = 0.0
        self.V_high_threshold = 0.001 # m^3
        self.T_low_threshold = 0.0
        self.T_high_threshold = 1000.0
        
        self.P_max = 20000000.0 # maximum pressure in the cylinder
        self.P_min = -10000000.0 # minimum pressure in the cylinder
        self.V_max = 0.002 # maximum volume of the cylinder
        self.V_min = -0.001 # minimum volume of the cylinder
        self.T_min = -100.0 # minimum temperature in the cylinder
        self.T_max = 1500.0 # maximum temperature in the cylinder
        
        self.T_low = 300.0 # temperature of the cold reservoir ~ room temperature
        self.T_high = 500.0 # temperature of the hot reservoir
        self.dV = 0.0005 # change in volume per 1 step
        
        # we initialize the state of the world with _reset() method 
        self.T = None  # temperature of gas 
        self.V = None  # volume of gas 
        self.P = None  # pressure
        self.state = None
        
        self.steps_beyond_done = None
        
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Box(
                                            low = np.array([self.T_min, self.V_min]), 
                                            high = np.array([self.T_max, self.V_max])
                                            )
        
        
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
        actions = ["push_T1", "push_T2", "push_N", 
                   "pull_T1", "pull_T2", "pull_N", 
                   "N_T1", "N_T2", "N_N"]
        
        state = self.state
        T_old, V_old = state
        done = False
        
        if actions[action] == "push_T1":
            self.T = self.T_low
            self.V = V_old - self.dV
            
            dW = self.N*self.R*self.T *np.log(self.V/V_old)
            dQ = 0 
            
            if np.abs(T_old - self.T_low)<50 and self.V > 0.0002:
                action_reward = 1000 
            else: 
                action_reward = -100000
            
        if actions[action] == "push_T2":
            self.T = self.T_high
            self.V = V_old - self.dV
            
            dW = self.N*self.R*self.T *np.log(self.V/V_old)
            dQ = 0 
            
            action_reward = -100000
        
        if actions[action] == "push_N":
            self.V = V_old - self.dV 
            self.T = T_old * math.pow(V_old/self.V, 2.0/3.0)
            
            dW = -3.0/2.0*self.N*self.R*(self.T - T_old)
            dQ = 0 
            
            if T_old >= self.T_low and T_old <= self.T_high and self.V <= 0.0021:
                action_reward = 1000
         
            else: 
                action_reward = -100000    
            
        if actions[action] == "pull_T1":
            
            self.T = self.T_low
            self.V = V_old + self.dV
            
            dW = self.N*self.R*self.T *math.log(self.V/V_old)
            dQ = 0 
            
            action_reward = -1000000
            
        if actions[action] == "pull_T2":
            self.T = self.T_high
            self.V = V_old + self.dV
            
            dW = self.N*self.R*self.T *math.log(self.V/V_old)
            dQ = dW 
            
            if np.abs(T_old - self.T_high) < 50 and self.V < 0.0005:
                action_reward = 1000
            else: 
                action_reward = -1000000
            
        if actions[action] == "pull_N":
           
            self.V = V_old + self.dV
            self.T = self.T * math.pow(V_old/self.V, 2.0/3.0)
            
            dW = -3.0/2.0*self.N*self.R*(self.T - T_old)
            dQ = 0 
            
            if T_old > self.T_low and T_old <= self.T_high and self.V >= 0.0005:
                action_reward = 1000
            
            else: 
                action_reward = -1000000
            
        if actions[action] == "N_T1":
            self.T = self.T_low
            self.V = V_old
            
            dW = 0
            dQ = 0 
            if T_old < self.T_low:
                action_reward = 1000
            else: 
                action_reward = -1000000
            
        if actions[action] == "N_T2": 
            self.T = self.T_high
            self.V = V_old
           
            dW = 0 
            dQ = 0
            
            if T_old > self.T_high:
                action_reward = 1000
            else: 
                action_reward = -1000000
            
        if actions[action] == "N_N":
            dW = 0 
            dQ = 0
            action_reward = -1000000
            
        self.__state_update__(self.T, self.V)
        
        done =    self.T < self.T_min or self.T > self.T_max \
               or self.P < self.P_min or self.P > self.P_max \
               or self.V < self.V_min or self.V > self.V_max
        done = bool(done)
        
        
        
        if  (     self.T < self.T_low_threshold or self.T > self.T_high_threshold \
               or self.P < self.P_low_threshold or self.P > self.P_high_threshold \
               or self.V < self.V_low_threshold or self.V > self.V_high_threshold    ):
            self.T = T_old
            self.V = V_old
            self.__state_update__(self.T, self.V)
            reward = 0.0 
        else:
            reward = action_reward
        
  #      if not done:
  #          reward = dW
  #      elif self.steps_beyond_done is None:
  #          # Episode just ended!
  #          self.steps_beyond_done = 0
  #          reward = -200.0
  #      else:
  #          if self.steps_beyond_done == 0:
  #              logger.warn("You are calling 'step()' even though this environment has already returned done = True. You     should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
  #          self.steps_beyond_done += 1
  #          reward = -200.0
        
        
        return np.array(self.state), reward, done, {'d_heat': dQ}   
  
    def __state_update__(self, T, V):
        '''
        Updates the state of the cylinder environment.
        '''
        self.T = T
        self.V = V
        self.P = self.N*T*self.R / V
        self.state = [self.T, self.V]

    def _reset(self):
        '''
        Resets the cylinder environment to its initial state.
        '''
       # T = np.random.rand()*200 + 300 
       # V = np.random.rand() * 0.0009 + 0.0001
       # self.__state_update__(T, V)
        self.__state_update__(300.0, 0.001)
        return np.array(self.state)
    
    def _render(self, mode='human', close=False):
        return