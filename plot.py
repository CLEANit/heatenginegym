import numpy as np
import matplotlib.pyplot as plt
import os

data1 = np.loadtxt('./champion.dat')

P1 = np.zeros(len(data1))
V1 = np.zeros(len(data1))
R1 = np.zeros(len(data1))

for i in range(len(data1)):
    P1[i] = data1[i][0]
    V1[i] = data1[i][1]
    R1[i] = data1[i][2]

for i in range(len(data1)):
    plt.figure(figsize=(12, 5))
    plt.title('Champion')
    plt.subplot(121)
    plt.plot(V1[:i+1], P1[:i+1], 'b-')
    plt.scatter(V1[i], P1[i], c = 'r')
    plt.xlim([0.0001, 0.0011])
    plt.ylim([110, 350])
    plt.subplot(122)
    plt.plot(np.arange(0, len(R1[:i+1]), 1), R1[:i+1], 'b-')
    plt.plot(np.arange(0, len(R1[:i+1]), 1), np.zeros(len(R1[:i+1])) + 0.4, 'k--')
    plt.xlim([0, len(data1)])
    plt.ylim([-1.0, 1.0])
    plt.savefig('./champion_movie/champion_' + str(i) + '.png', dpi=300)
    plt.close()
