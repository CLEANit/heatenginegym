import numpy as np
from grid_policy import Policy

def selection(population, scores):
    p = scores / scores.sum()
    i = np.random.choice(range(len(population)), p = p)
    j = i
    while i == j:
        j = np.random.choice(range(len(population)), p = p)

    return population[i], population[j]

def crossover(policy1, policy2, p = 0.5):
    new_policy = Policy(policy1.num_actions)
    for i in range(int(len(policy1.policy) * p)):
        for j in range(len(policy1.policy[i])):
            new_policy.policy[i][j] = policy1.policy[i][j]

    for i in range(int(len(policy2.policy) * (1.0 - p)), len(policy2.policy)):
        for j in range(len(policy2.policy[i])):
            new_policy.policy[i][j] = policy2.policy[i][j]

    return new_policy

def mutation(policy, p = 0.05):
    new_policy = Policy(policy.num_actions)
    for i in range(len(policy.policy)):
        for j in range(len(policy.policy[i])):
            r = np.random.uniform()
            if r < p:
                new_policy.policy[i][j] = np.random.randint(0, policy.num_actions)
            else:
                new_policy.policy[i][j] = policy.policy[i][j]

    return new_policy

def evaluate_policy(policy, env):
    reward = 0
    for i in range(3):
        s = env.reset()
        d = False
        while not d:
            a = policy.evaluate(s)
            s, r, d, _ = env.step(a)

        reward += r
    reward = reward / 3.0

    return reward

def vis_policy(policy, env):
    s = env.reset()
    d = False
    while not d:
        a = policy.evaluate(s)
        s, r, d, p = env.step(a)
        print p, s[1], r
