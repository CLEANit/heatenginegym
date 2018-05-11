import numpy as np

class Engine:
    def __init__(self, Ti = 300.0, Vi = 0.001, Tc = 300.0, Th = 500.0, dV = 0.0002):
        self.N = 1.0/22.4 # 1 mole occupies 22.4 L at STP
        self.c = 5.0/3.0  # Type of gas 
        self.R = 8.3144598/1000.0 # Units of kJ/K/mol

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
        self.P = self.N * self.T * self.R / self.V

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

        dW = -(3.0/2.0) * self.N * self.R * (self.T - T)
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def N_Tc(self):
        self.T = self.Tc

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

        dW = self.N * self.R * self.T * np.log(self.V / V)
        dQ = 0.0
        return self.T, self.V, dW, dQ

    def N_Th(self):
        self.T = self.Th

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

        dW = self.N * self.R * self.T * np.log(self.V / V)
        dQ = 0.0
        return self.T, self.V, dW, dQ

class Cycle:
    def __init__(self):
        self.engine = Engine()

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

    def reset(self):
        self.engine.reset()
        return np.array([self.engine.T, self.engine.V])

    def step(self, action):
        self.engine.T, self.engine.V, self.dW, self.dQ = self.actions[action]()
        return np.array([self.engine.T, self.engine.V]), self.dW, self.done, self.dQ
