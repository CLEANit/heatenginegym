import numpy as np
import gym

class Engine:
    def __init__(self, Ti=300.0, Vi=0.001, Tc=300.0, Th=500.0, dV=0.0002):
        self.N = 1.0/22.4 # 1 mole occupies 22.4 L at STP
        self.c = 5.0/3.0  # Type of gas 
        self.kB = 1.38064852e-23  #Boltzmann constant
        self.NA = 6.0221409e+23   #Avogadro's number

        self.J_to_kJ = 0.001

        self.R = self.kB * self.NA * self.J_to_kJ # Units of kJ/K/mol

        self.Vmin = 0.0001 # m**3
        self.Vmax = 0.001 # m**3
        self.Tmin = 0.0 # K
        self.Tmax = 1000.0 # K

        self.Ti = Ti # Initial T
        self.Vi = Vi # Initial V
        self.Tc = Tc # T of Cold Reservoir
        self.Th = Th # T of Hot Reservoir
        self.dV = dV # Change in V

        self.T = self.Ti
        self.V = self.Vi
        self.__update_equations_of_state()

    def __update_equations_of_state(self):
        self.P = self.N * self.T * self.R / self.V
        self.U = 3./2. * self.N * self.NA * self.kB * self.T

    def reset(self):
        self.T = self.Ti
        self.V = self.Vi
        self.P = self.N * self.T * self.R / self.V

    def N_D(self):
        dW = 0.0
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def push_D(self):
        V = self.V
        T = self.T
        self.V -= self.dV
        if self.V <= self.Vmin:
            self.V = V
        self.T = T * ((V/self.V) ** (2.0/3.0))
        self.__update_equations_of_state()

        dW = -(3.0/2.0) * self.N * self.R * (self.T - T)
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def pull_D(self):
        V = self.V
        T = self.T
        self.V += self.dV
        if self.V > self.Vmax:
            self.V = V
        self.T = T * ((V/self.V) ** (2.0/3.0))
        self.__update_equations_of_state()

        dW = -(3.0/2.0) * self.N * self.R * (self.T - T)
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def N_Tc(self):
        self.T = self.Tc
        self.__update_equations_of_state()

        dW = 0.0
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def push_Tc(self):
        V = self.V
        T = self.T
        self.V -= self.dV
        if self.V <= self.Vmin:
            self.V = V
        self.T = self.Tc
        self.__update_equations_of_state()

        dW = self.N * self.R * self.T * np.log(self.V / V)
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def pull_Tc(self):
        V = self.V
        T = self.T
        self.V += self.dV
        if self.V > self.Vmax:
            self.V = V
        self.T = self.Tc

        self.__update_equations_of_state()
        dW = self.N * self.R * self.T * np.log(self.V / V)
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def N_Th(self):
        self.T = self.Th
        self.__update_equations_of_state()

        dW = 0.0
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def push_Th(self):
        V = self.V
        T = self.T
        self.V -= self.dV
        if self.V <= self.Vmin:
            self.V = V
        self.T = self.Th

        self.__update_equations_of_state()
        dW = self.N * self.R * self.T * np.log(self.V / V)
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def pull_Th(self):
        V = self.V
        T = self.T
        self.V += self.dV
        if self.V > self.Vmax:
            self.V = V
        self.T = self.Th

        self.__update_equations_of_state()
        dW = self.N * self.R * self.T * np.log(self.V / V)
        dQ = dW
        return self.T, self.V, dW, dQ

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


    def get_perfect_carnot_action_set(self):
        VA = self.engine.Vmin
        VD = VA * (self.engine.Th / self.engine.Tc)**(3./2.)
        VC = self.engine.Vmax
        VB = VC * (self.engine.Tc / self.engine.Th)**(3./2.)

        N1, N2, N3, N4 = [int( abs(VC-VD)/self.engine.dV),int( abs(VD-VA)/self.engine.dV),int( abs(VB-VA)/self.engine.dV),int( abs(VC-VB)/self.engine.dV)]
        print N1, N2, N3, N4
        actions = ['push_Tc']*N1 + ['push_D']*N2 + ['pull_Th']*N3 + ['pull_D']*N4 + \
                  ['push_Tc']*N1 + ['push_D']*N2 + ['pull_Th']*N3 + ['pull_D']*N4 + \
                  ['push_Tc']*N1 + ['push_D']*N2 + ['pull_Th']*N3 + ['pull_D']*N4 + \
                  ['push_Tc']*N1 + ['push_D']*N2 + ['pull_Th']*N3 + ['pull_D']*N4 + \
                  ['push_Tc']*N1 + ['push_D']*N2 + ['pull_Th']*N3 + ['pull_D']*N4 + \
                  ['push_Tc']*N1 + ['push_D']*N2 + ['pull_Th']*N3 + ['pull_D']*N4 + \
                  ['push_Tc']*N1 + ['push_D']*N2 + ['pull_Th']*N3 + ['pull_D']*N4
        self.engine.Pmax = self.engine.N * self.engine.R * self.engine.Th / VA
        self.engine.Pmin = self.engine.N * self.engine.R * self.engine.Tc / VC



        return actions

    def reset(self):
        self.engine.reset()
        self.Q = []
        self.W = []
        return np.array([self.engine.T, self.engine.V])

    def step(self, action):
        self.engine.T, self.engine.V, self.dW, self.dQ = self.actions[action]()
        self.Q.append(self.dQ)
        self.W.append(self.dW)
        return np.array([self.engine.T, self.engine.V]), self.dW, self.done, self.dQ
