import gym
import gym.spaces
import cleangym
from cleangym.scores import Scores
import numpy as np
from grid_helper import *
from grid_policy import Policy
from multiprocessing import Pool
import os

if not os.path.exists('./grid_champions'):
    os.makedirs('./grid_champions')

n_gen = 1000 # Number of generations
n_pop = 100 # Starting population
n_mutate = 25 # Number of mutations per generation
n_breed = 25 # Number of crossovers per generation
n_sacrifice = 50 # Number of removals per generation
game = 'Carnot-v0' # Game to play
cpus = 4 # Number of processes to run
pool = Pool(processes = cpus)
min_score, max_score = Scores(game)

env = gym.make(game)
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
    policy = Policy(num_actions, game)
    policy.gen_random()
    population.append(policy)

gen = 0
winning = False

for generation in range(n_gen):
    gen += 1
    scores = pool.map(evaluate_policy, population)

    l1, l2 = zip(*sorted(zip(scores, population), key = lambda x: x[0]))
    scores = np.array(l1[n_sacrifice:])
    population = list(l2[n_sacrifice:])
    population[-1].win += 1
    print('Generation %d: Average Score = %0.2f, Max Score = %0.2f, Policy Wins = %i, Population Size = %i' %(gen, np.mean(scores), scores[-1], population[-1].win, n_pop))
    n_pop -= n_sacrifice

    if gen % 100 == 0:
        champion = population[-1]
        np.savez('./grid_champions/' + game + '_' + str(gen) + '.npz', w=champion.policy)
        print('Champion has won ' + str(champion.win) + ' game(s)!')

    choice = np.ones(len(scores))
    cross_pop = []
    mutate_pop = []
    for i in range(n_breed):
        policy1, policy2 = selection(population, choice)
        cross_pop.append([policy1, policy2])

    for i in range(n_mutate):
        policy1, policy2 = selection(population, choice)
        mutate_pop.append([policy1])

    younglings = pool.map(crossover, cross_pop)
    mutants = pool.map(mutation, mutate_pop)

    n_pop += n_breed
    n_pop += n_mutate

    population += younglings
    population += mutants

scores = pool.map(evaluate_policy, population)

print('Best policy score = %0.2f.' %(np.max(scores)))

l1, l2 = zip(*sorted(zip(scores, population), key = lambda x: x[0]))
champion = l2[-1]
champion.win += 1
np.savez('./grid_champions/' + game + '_' + str(gen) + '.npz', w=champion.policy)
print('Champion has won ' + str(champion.win) + ' game(s)!')
