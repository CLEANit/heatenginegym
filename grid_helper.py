import numpy as np
from grid_policy import Policy

def selection(population, scores):
    p = scores / scores.sum()
    i = np.random.choice(range(len(population)), p = p)
    j = i
    while i == j:
        j = np.random.choice(range(len(population)), p = p)

    r = np.random.uniform()
    if r < 0.5:
        return population[i], population[j]
    else:
        return population[j], population[i]

def crossover(cross_pop, p = 0.5):
    policy1 = cross_pop[0]
    policy2 = cross_pop[1]
    new_policy = Policy(policy1.num_actions, policy1.game)
    for i in range(int(len(policy1.policy) * p)):
        for j in range(len(policy1.policy[i])):
            new_policy.policy[i][j] = policy1.policy[i][j]

    for i in range(int(len(policy2.policy) * (1.0 - p)), len(policy2.policy)):
        for j in range(len(policy2.policy[i])):
            new_policy.policy[i][j] = policy2.policy[i][j]

    return new_policy

def mutation(mutate_pop, p = 0.10):
    policy = mutate_pop[0]
    new_policy = Policy(policy.num_actions)
    for i in range(len(policy.policy)):
        for j in range(len(policy.policy[i])):
            r = np.random.uniform()
            if r < p:
                new_policy.policy[i][j] = np.random.randint(0, policy.num_actions)
            else:
                new_policy.policy[i][j] = policy.policy[i][j]

    return new_policy

def evaluate_policy(policy):
    env = policy.env
    reward = 0
    for i in range(3):
        s = env.reset()
        count = 0
        d = False
        while not d:
            a = policy.evaluate(s)
            #s, r, d, _ = env.step(a)
            s1, r, d, _ = env.step(a)
            if np.array_equal(s,s1):
                count -= 0.01
            s = s1
          
        reward += r + count
    reward = reward / 3.0

    return reward

def vis_policy(policy, env):
    s = env.reset()
    d = False
    while not d:
        a = policy.evaluate(s)
        s, r, d, p = env.step(a)
        print(p, s[1], r)
