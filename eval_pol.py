import numpy as np
import gym
import gym.spaces
import cleangym
from policy import Policy
from helper import *
import matplotlib.pyplot as plt

game = 'MountainCar-v0'
gen = 100
data = np.load('./champions/' + game + '_' + str(gen) + '.npz')

env = gym.make(game)
num_actions = int(env.action_space.n)
s0 = env.reset()
try:
    s0 = np.reshape(s0, (s0.shape[0], 1))
except ValueError:
    s0 = s0

shape = s0.shape
hidden_units = data['h']

champion = Policy(shape, hidden_units, num_actions, game)
champion.W = data['w']
champion.B = data['b']

score = 0.0
for i in range(10):
    score += evaluate_policy(champion)

score = score / 10.0
print('Champion Average Score = ' + str(score))

for i in range(1):
    vis_policy(champion)

