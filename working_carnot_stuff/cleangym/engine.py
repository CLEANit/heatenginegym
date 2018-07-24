import numpy as np
import gym

class Engine(object):
    def __init__(self, Ti=300.0, Vi=0.001, Tc=300.0, Th=500.0, dV=0.00002):
        self.N = 1.0/22.4 # 1 mole occupies 22.4 L at STP
        self.c = 5.0/3.0  # Type of gas 
        self.kB = 1.38064852e-23  #Boltzmann constant
        self.NA = 6.0221409e+23   #Avogadro's number

        self.J_to_kJ = 0.001

        self.R = self.kB * self.NA * self.J_to_kJ # Units of kJ/K/mol

        self.Vmin = 0.0001 # m**3
        self.Vmax = 0.001
        #self.Vmax = 0.001 # m**3
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
        if self.V < self.Vmin:
            self.V = V
        self.T = T * ((V/self.V) ** (2.0/3.0))
        if self.T > self.Tmax:
            self.T = T
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
        if self.T < self.Tmin:
            self.T = T
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
        T = self.T 
        self.T = self.Th
        self.__update_equations_of_state()

        dW = 0.0
        if T < self.Th:
            dQ = (3.0/2.0) * self.N * self.R * (self.Th - T)
        else:
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
        
        if T < self.Th:
            dQ = (3.0/2.0) * self.N * self.R * (self.Th - T)
        else:
            dQ = 0
            
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
        
        if T < self.Th:
            dQ = dW + (3.0/2.0) * self.N * self.R * (self.Th - T)
        else:
            dQ = dW
        return self.T, self.V, dW, dQ


