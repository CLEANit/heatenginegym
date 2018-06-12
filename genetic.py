import gym
import gym.spaces
import cleangym
import numpy as np
from helper import *
from policy import Policy
import os

if not os.path.exists('./champions'):
    os.makedirs('./champions')

n_gen = 1000000 # Number of generations
n_pop = 100 # Starting population
n_mutate = 25 # Number of mutations per generation
n_breed = 25 # Number of crossovers per generation
n_sacrifice = 50 # Number of removals per generation
hidden_units = np.array([128, 128]) # Number of kernels per layer, len(hidden_units) = number of layers
cross_p = 0.5 # Probability of policy1 weight being used during crossover
mut_p = 0.5 # Probability of weight mutating
wins = 10 # Number of wins to be considered the best
game = 'Carnot-v0' # Game to play

env = gym.make(game)
s0 = env.reset()
s0 = np.reshape(s0, (s0.shape[0], 1))
num_actions = int(env.action_space.n)

name = 0
if n_sacrifice > n_mutate + n_breed:
    n_sacrifice = n_mutate + n_breed
    print ('Sacrifice > growth per generation. n_sacrifice lowered to ' + str(n_sacrifice))
if n_pop <= 2:
    n_sacrifice = 0
    print ('Not enough population to sacrifice. n_sacrifice lowered to ' + str(n_sacrifice))
elif n_sacrifice >= n_pop - 1:
    n_sacrifice = n_pop - 2
    print ('Sacrifice too large. n_sacrifice lowered to ' + str(n_sacrifice))

population = []
for i in range(n_pop):
    policy = Policy(s0, hidden_units, num_actions)
    policy.gen_random()
    population.append(policy)

gen = 0
winning = False

for generation in range(n_gen):
    gen += 1
    scores = np.zeros(n_pop)
    for i in range(n_pop):
        scores[i] = evaluate_policy(population[i], env)

    l1, l2 = zip(*sorted(zip(scores, population)))
    scores = np.array(l1[n_sacrifice:])
    population = list(l2[n_sacrifice:])
    population[-1].win += 1
    print('Generation %d: Average Score = %0.2f, Max Score = %0.2f, Policy Wins = %i, Population Size = %i' %(gen, np.mean(scores), scores[-1], population[-1].win, n_pop))
    n_pop -= n_sacrifice

    if gen % 100 == 0:
        champion = population[-1]
        np.savez('./champions/' + game + '_' + str(gen) + '.npz', w=champion.W, b=champion.B)
        print('Champion has won ' + str(champion.win + 1) + ' game(s)!')

    scores += 1.1
    younglings = []
    mutants = []
    for i in range(n_breed):
        policy1, policy2 = selection(population, scores)
        new_policy = crossover(policy1, policy2, cross_p)
        younglings.append(new_policy)

    n_pop += n_breed

    for i in range(n_mutate):
        policy1, policy2 = selection(population, scores)
        new_policy = mutation(policy1, mut_p)
        mutants.append(new_policy)

    n_pop += n_mutate

    population += younglings
    population += mutants

scores = np.zeros(n_pop)
for i in range(n_pop):
    scores[i] = evaluate_policy(population[i], env)

print('Best policy score = %0.2f.' %(np.max(scores)))

l1, l2 = zip(*sorted(zip(scores, population),key=lambda x: x[0]))
champion = l2[-1]
champion.win += 1
np.savez('./champions/' + game + '.npz', w=champion.W, b=champion.B)
print('Champion has won ' + str(champion.win) + ' game(s)!')
