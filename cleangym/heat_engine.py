import numpy as np
import gym
import gym.spaces
from cleangym.engine import Engine
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pylab import cm
class HeatEngineEnv(gym.Env):
    def __init__(self, *args, **kwargs):
        self.engine = Engine(*args, **kwargs)
        self.done = False
        self.Q = []
        self.W = []
        self._first_render = True
        self._plot_data_persistent = {"r":[]}
        self._max_episode_steps = 100000

    def reset(self):
        self.engine.reset()
        self.done = False
        self.Q = []
        self.W = []
        T = (self.engine.T - self.engine.Tmin) / (self.engine.Tmax - self.engine.Tmin)
        V = (self.engine.V - self.engine.Vmin) / (self.engine.Vmax - self.engine.Vmin)
        self._plot_data = {"P" : [self.engine.P], "V": [self.engine.V], "r":[0] }
        self._first_render=True
        self._plot_data_persistent["r"].append(0)
        return np.array([T, V])


    def render(self, mode='plot'):
        pv_points_to_plot = 12
        if self._first_render:
            plt.xkcd()
            plt.close('all')
            plt.ion()
            self._plot_fig, self._plot_axs = plt.subplots(1,2,figsize=(12,6))
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
            self._plot_li0.set_xdata(self._plot_data['V'][:])
            self._plot_li0.set_ydata(self._plot_data['P'][:])
            self._plot_li1.set_xdata(np.arange(len(self._plot_data["r"])))
            self._plot_li1.set_ydata(self._plot_data["r"])
            for  i in reversed(range(1,len(self._plot_li0_masks))):
                self._plot_li0_masks[i].set_xdata(self._plot_data['V'][-i:])
                self._plot_li0_masks[i].set_ydata(self._plot_data['P'][-i:])


            for ax in [self._plot_axs[1]]:
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
            r = 0.0
        T = (self.engine.T - self.engine.Tmin) / (self.engine.Tmax - self.engine.Tmin)
        V = (self.engine.V - self.engine.Vmin) / (self.engine.Vmax - self.engine.Vmin)
        self._plot_data['P'].append(self.engine.P)
        self._plot_data['V'].append(self.engine.V*1000.)
        self._plot_data['r'].append(r)
        self._plot_data_persistent['r'][-1] += r
        return np.array([T, V]), r, self.done, np.array([self.engine.T, self.engine.V, self.engine.P])

