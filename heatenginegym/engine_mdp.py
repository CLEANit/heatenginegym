import numpy as np
import gym
from scipy.integrate import quad

class Engine(object):
    def __init__(self, Ti=300.0, Vi=0.001, Tc=300.0, Th=500.0, dV=0.0002, k=0.0):
        self.N = 1.0/22.4 # 1 mole occupies 22.4 L at STP
        self.c = 5.0/3.0  # Type of gas 
        self.kB = 1.38064852e-23  #Boltzmann constant
        self.NA = 6.0221409e+23   #Avogadro's number

        self.J_to_kJ = 0.001

        self.R = self.kB * self.NA * self.J_to_kJ # Units of kJ/K/mol

        self.Cv = (3.0/2.0) * self.N * self.R # Cv for this type of gas

        self.Vmin = 0.0002 # m**3
        self.Vmax = 0.001 # m**3
        self.Tmin = Tc # K
        self.Tmax = Th # K

        self.Pmin = self.N*self.R*self.Tmin / self.Vmax
        self.Pmax = self.N*self.R*self.Tmax / self.Vmin

        self.Ti = Ti # Initial T
        self.Vi = Vi # Initial V
        self.Tc = Tc # T of Cold Reservoir
        self.Th = Th # T of Hot Reservoir
        self.dV = dV # Change in V
        self.dVi = dV # Initial Change in V
        self.k = k # Fraction of heat loss

        self.T = self.Ti
        self.V = self.Vi
        self.__update_equations_of_state()
        self.P0 = self.P
        self.V0 = self.V
        self.T0 = self.T

    def __update_equations_of_state(self):
        self.P = self.N * self.T * self.R / self.V
        self.U = 3./2. * self.N * self.NA * self.kB * self.T

    def _P_L(self, V):
        return self.P0 * (self.V0 ** (5.0/3.0)) * ((1.0 - self.k) ** (abs(V - self.V0) / (self.Vmax - self.Vmin))) / (V ** (5.0 / 3.0))

    def reset(self):
        self.T = self.Ti
        self.V = self.Vi
        self.dV = self.dVi
        self.P = self.N * self.T * self.R / self.V

    def reverse(self):
        self.T = self.T0
        self.V = self.V0

    def N_D(self):
        dW = 0.0
        dQ = 0.0
        
        return self.T, self.V, dW, dQ, True

    def push_D(self):
        self.V0 = self.V
        self.T0 = self.T
        self.V -= self.dV
        if self.V - self.Vmin < -1e-9:
            self.V = self.Vmin
        self.T = self.T0 * ((self.V0/self.V) ** (2.0/3.0))
        if self.T - self.Tmax > 1e-9:
            self.T = self.T0
            self.V = self.V0
        self.__update_equations_of_state()

        dW = -(3.0/2.0) * self.N * self.R * (self.T - self.T0)
        dQ = 0.0
        
        return self.T, self.V, dW, dQ, False

    def pull_D(self):
        self.V0 = self.V
        self.T0 = self.T
        self.V += self.dV
        if self.V - self.Vmax > 1e-9:
            self.V = self.Vmax
        self.T = self.T0 * ((self.V0/self.V) ** (2.0/3.0))
        if self.T - self.Tmin < -1e-9:
            self.T = self.T0
            self.V = self.V0
        self.__update_equations_of_state()

        dW = -(3.0/2.0) * self.N * self.R * (self.T - self.T0)
        dQ = 0.0
        
        return self.T, self.V, dW, dQ, False

    def push_L(self):
        self.V0 = self.V
        self.T0 = self.T
        self.P0 = self.P
        self.V -= self.dV
        if self.V - self.Vmin < -1e-9:
            self.V = self.Vmin
        if abs(self.V - self.V0) < 1e-9:
            self.T = self.T0 * (self.V0 ** (2.0/3.0)) * ((1.0 - self.k) ** (abs(self.V - self.V0) / (self.Vmax - self.Vmin))) / ((self.V) ** (2.0/3.0))
        if self.T - self.Tmax > 1e-9 or self.T - self.Tmin < -1e-9:
            self.T = self.T0
            self.V = self.V0
        self.__update_equations_of_state()

        dW = quad(self._P_L, self.V0, self.V)[0]
        dQ = 0.0

        return self.T, self.V, dW, dQ, False

    def pull_L(self):
        self.V0 = self.V
        self.T0 = self.T
        self.P0 = self.P
        self.V += self.dV
        if self.V - self.Vmax > 1e-9:
            self.V = self.Vmax
        if abs(self.V - self.V0) < 1e-9:
            self.T = self.T0 * (self.V0 ** (2.0/3.0)) * ((1.0 - self.k) ** (abs(self.V - self.V0) / (self.Vmax - self.Vmin))) / ((self.V) ** (2.0/3.0))
        if self.T - self.Tmax > 1e-9 or self.T - self.Tmin < -1e-9:
            self.T = self.T0
            self.V = self.V0
        self.__update_equations_of_state()

        dW = quad(self._P_L, self.V0, self.V)[0]
        dQ = 0.0

        return self.T, self.V, dW, dQ, False

    def N_Tc(self):
        self.T = self.Tc
        self.__update_equations_of_state()

        dW = 0.0
        dQ = 0.0
        
        return self.T, self.V, dW, dQ, False

    def push_Tc(self):
        self.V0 = self.V
        self.V -= self.dV
        if self.V - self.Vmin < -1e-9:
            self.V = self.Vmin
        self.T = self.Tc
        self.__update_equations_of_state()

        dW = self.N * self.R * self.T * np.log(self.V / self.V0)
        dQ = 0.0

        return self.T, self.V, dW, dQ, False

    def pull_Tc(self):
        self.V0 = self.V
        self.V += self.dV
        if self.V - self.Vmax > 1e-9:
            self.V = self.Vmax
        self.T = self.Tc

        self.__update_equations_of_state()
        dW = self.N * self.R * self.T * np.log(self.V / self.V0)
        dQ = 0.0
        return self.T, self.V, dW, dQ, False

    def N_Th(self):
        self.T0 = self.T
        self.T = self.Th
        self.__update_equations_of_state()

        dW = 0.0
        if self.T0 - self.Th < -1e-9:
            dQ = (3.0/2.0) * self.N * self.R * (self.Th - self.T0)
        else:
            dQ = 0.0
        
        return self.T, self.V, dW, dQ, False

    def push_Th(self):
        self.V0 = self.V
        self.T0 = self.T
        self.V -= self.dV
        if self.V - self.Vmin < -1e-9:
            self.V = self.Vmin
        self.T = self.Th

        self.__update_equations_of_state()
        dW = self.N * self.R * self.T * np.log(self.V / self.V0)
        
        if self.T0 - self.Th < -1e-9:
            dQ = (3.0/2.0) * self.N * self.R * (self.Th - self.T0)
        else:
            dQ = 0
            
        return self.T, self.V, dW, dQ, False

    def pull_Th(self):
        self.V0 = self.V
        self.T0 = self.T
        self.V += self.dV
        if self.V - self.Vmax > 1e-9:
            self.V = self.Vmax
        self.T = self.Th
        
        self.__update_equations_of_state()
        dW = self.N * self.R * self.T * np.log(self.V / self.V0)
        
        if self.T0 - self.Th < -1e-9:
            dQ = dW + (3.0/2.0) * self.N * self.R * (self.Th - self.T0)
        else:
            dQ = dW

        return self.T, self.V, dW, dQ, False


