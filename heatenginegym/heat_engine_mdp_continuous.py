import numpy as np
import gym
import gym.spaces
from heatenginegym.engine_mdp import Engine
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pylab import cm
import collections

class HeatEngineEnv(gym.Env):
    def __init__(self, max_episode_steps=200, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)
        self.done = False
        self.Qi = 0.7824495820293804
        self.Wi = 0.3
        self.t = 0
        self._first_render = True
        self._plot_data_persistent = {"r":[]}
        self._max_episode_steps = max_episode_steps

    def reset(self):
        self.engine.reset()
        self.done = False
        self.Q = self.Qi
        self.W = self.Wi
        self.t = 0
        self._plot_data = {"P" : [self.engine.P],
                           "V" : [self.engine.V*1000.0],
                           "r" : [np.nan],
                           "dQ": [0.],
                           "dW": [0.],}
        self._first_render=True
        return np.array([self.engine.T, self.engine.V, self.Q, self.W])


    def render(self, mode='plot'):
        pv_points_to_plot = 12
        if self._first_render:
            plt.xkcd()
            plt.close('all')
            plt.ion()
            self._plot_fig, self._plot_axs = plt.subplots(1,3,figsize=(12,4))
            self._plot_li0_masks = []
            self._plot_li0, = self._plot_axs[0].plot(self._plot_data['V'][:], self._plot_data['P'][:], 'o-', color='white')
            cs = cm.get_cmap('Blues',11)
            for i in reversed(range(1,pv_points_to_plot)):
                self._plot_li0_masks.append(
                            #self._plot_axs[0].plot(self._plot_data['V'][-pv_points_to_plot:-pv_points_to_plot+i], self._plot_data['P'][-pv_points_to_plot:-pv_points_to_plot+i], 'o-',
                            self._plot_axs[0].plot(self._plot_data['V'][-i:-i+2], self._plot_data['P'][-i:-i+2], 'o-',
                            color=cs(i/12.), linewidth=3,zorder=i*100)[0]
                     )

            self._plot_li1, = self._plot_axs[1].plot(np.arange(len(self._plot_data["r"])), self._plot_data["r"], 'g-')
            self._plot_dq_line, = self._plot_axs[2].plot(np.arange(len(self._plot_data["dQ"])), self._plot_data["dQ"], alpha=0.8, label='dQ')
            self._plot_dw_line, = self._plot_axs[2].plot(np.arange(len(self._plot_data["dW"])), self._plot_data["dW"], alpha=0.8, label='dW')
            self._plot_axs[2].legend()
            self._plot_axs[1].axhline(y=self.efficiency, color='red', ls='--')

            self._plot_axs[0].set_xlabel("Volume [L]")
            self._plot_axs[0].set_ylabel("Pressure ")
            vr = abs(self.engine.Vmin-self.engine.Vmax)
            pr = abs(self.engine.Pmin-self.engine.Pmax)
            self._plot_axs[0].add_patch(Rectangle((self.engine.Vmin*1000, self.engine.Pmin), vr*1000., pr, color='#DDDDDD'))
            self._plot_axs[0].set_xlim([(self.engine.Vmin-0.1*vr)*1000, (self.engine.Vmax+0.1*vr)*1000])
            self._plot_axs[0].set_ylim([self.engine.Pmin-0.1*pr, self.engine.Pmax+0.1*pr])
            self._plot_axs[1].set_xlabel("Step")
            self._plot_axs[1].set_ylabel("Efficiency")
            plt.tight_layout()
            self._plot_fig.canvas.draw()
            plt.show()
            self._first_render = False

        else:
            self._plot_dq_line.set_xdata(np.arange(len(self._plot_data["dQ"])))
            self._plot_dq_line.set_ydata(self._plot_data["dQ"])
            self._plot_dw_line.set_xdata(np.arange(len(self._plot_data["dW"])))
            self._plot_dw_line.set_ydata(self._plot_data["dW"])
            self._plot_li0.set_xdata(self._plot_data['V'][:])
            self._plot_li0.set_ydata(self._plot_data['P'][:])
            self._plot_li1.set_xdata(np.arange(len(self._plot_data["r"])))
            self._plot_li1.set_ydata(self._plot_data["r"])
            for  i in reversed(range(1,len(self._plot_li0_masks))):
                self._plot_li0_masks[i].set_xdata(self._plot_data['V'][-i:])
                self._plot_li0_masks[i].set_ydata(self._plot_data['P'][-i:])

            for ax in [self._plot_axs[1], self._plot_axs[2]]:
                ax.relim()
                ax.autoscale_view(True, True, True)
            self._plot_fig.canvas.draw()
            plt.pause(0.000001)

    def step(self, action):
        action1 = int(action[0])
        action2 = action[1] 
        self.engine.dV = action2
        self.engine.T, self.engine.V, self.dW, self.dQ, self.done = self.actions[action1]()
        if (self.Q - self.dQ) > -1e-9 and (self.W + self.dW) > -1e-9:
            self.Q -= self.dQ
            self.W += self.dW
        else:
            self.engine.reverse()
        self.t += 1
        if self.t == self._max_episode_steps:
            self.done = True
        if self.done:
            r = self.W - self.Wi
        else:
            r = 0.0
        try:
            eta = float(self.W - self.Wi) / float(self.Qi - self.Q)
        except ZeroDivisionError:
            eta = 0.0
        self._plot_data['P'].append(self.engine.P)
        self._plot_data['V'].append(self.engine.V*1000.)
        self._plot_data['r'].append(eta)
        self._plot_data['dQ'].append(self.dQ)
        self._plot_data['dW'].append(self.dW)

        return np.array([self.engine.T, self.engine.V, self.Q, self.W]), r, self.done, {}

