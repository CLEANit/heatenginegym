import gym
import cleangym
import time
import matplotlib.pyplot as plt

env = gym.make('Carnot-v1')
env.reset()

i = 0
As =  env.unwrapped.get_perfect_action_set(cycles=10)
for A in As:
    state, reward, done, _ = env.step(env.unwrapped.action_map[A])
    i+=1
    env.render()
    time.sleep(0.001)
    print(i,reward,done)
