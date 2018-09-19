import numpy as np
import gym
import gym.spaces
from cleangym.engine import Engine
import matplotlib.pyplot as plt

class HeatEngineEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)
        self.done = False
        self.Q = []
        self.W = []
        self._first_render = True

    def reset(self):
        self.engine.reset()
        self.Q = []
        self.W = []
        T = (self.engine.T - self.engine.Tmin) / (self.engine.Tmax - self.engine.Tmin)
        V = (self.engine.V - self.engine.Vmin) / (self.engine.Vmax - self.engine.Vmin)
        self._plot_data = {"P" : [self.engine.P], "V": [self.engine.V], "r":[0] }
        self._first_render=True
        return np.array([T, V])


    def render(self, mode='plot'):
        if self._first_render:
            plt.xkcd()
            plt.close('all')
            plt.ion()
            self._plot_fig, self._plot_axs = plt.subplots(1,2,figsize=(8,3))
            self._plot_li0, = self._plot_axs[0].plot(self._plot_data['V'], self._plot_data['P'], 'o--')
            self._plot_li1, = self._plot_axs[1].plot(np.arange(len(self._plot_data["r"])), self._plot_data["r"], 'g-')
            self._plot_axs[1].axhline(y=self.efficiency, color='red', ls='--') #np.arange(len(self._plot_data["r"])), np.zeros_like(np.arange(len(self._plot_data["r"])))+self.efficiency, 'r-')
            self._plot_axs[0].set_xlabel("Volume")
            self._plot_axs[0].set_ylabel("Pressure")
            self._plot_axs[1].set_xlabel("Step")
            self._plot_axs[1].set_ylabel("Efficiency")
            plt.tight_layout()
            self._plot_fig.canvas.draw()
            plt.show()
            self._first_render = False

        else:
            self._plot_li0.set_xdata(self._plot_data['V'])
            self._plot_li0.set_ydata(self._plot_data['P'])
            self._plot_li1.set_xdata(np.arange(len(self._plot_data["r"])))
            self._plot_li1.set_ydata(self._plot_data["r"])
            for ax in [self._plot_axs[0], self._plot_axs[1]]:
                ax.relim()
                ax.autoscale_view(True, True, True)
            self._plot_fig.canvas.draw()
            plt.pause(0.000001)

    def step(self, action):
        self.engine.T, self.engine.V, self.dW, self.dQ = self.actions[action]()
        self.Q.append(self.dQ)
        self.W.append(self.dW)
        try:
            r = float(np.array(self.W).sum()) / float(np.array(self.Q).sum())
        except ZeroDivisionError:
            r = -1.0
        T = (self.engine.T - self.engine.Tmin) / (self.engine.Tmax - self.engine.Tmin)
        V = (self.engine.V - self.engine.Vmin) / (self.engine.Vmax - self.engine.Vmin)
        self._plot_data['P'].append(self.engine.P)
        self._plot_data['V'].append(V)
        self._plot_data['r'].append(r)
        return np.array([T, V]), r, self.done, np.array([self.engine.T, self.engine.V, self.engine.P])

