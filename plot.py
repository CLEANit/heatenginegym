import numpy as np
import matplotlib.pyplot as plt
import os

data1 = np.loadtxt('./champion.dat')

P1 = np.zeros(len(data1))
V1 = np.zeros(len(data1))
R1 = np.zeros(len(data1))
A1 = np.zeros(len(data1), dtype=np.int32)

colors = ['m-', 'b-', 'k-', 'g-']

for i in range(len(data1)):
    P1[i] = data1[i][0]
    V1[i] = data1[i][1]
    R1[i] = data1[i][2]
    A1[i] = int(data1[i][3])

j = 0
for i in range(len(data1)):
    if i % 1 == 0:
        plt.figure(figsize=(12, 5))

        plt.subplot(121)
        plt.plot(V1[:i+1], P1[:i+1], 'b-')
        plt.scatter(V1[i], P1[i], c = 'r')
        plt.xlim([0.0001, 0.0011])
        plt.ylim([np.min(P1), np.max(P1)])
        plt.xlabel('Volume')
        plt.ylabel('Pressure')

        plt.subplot(122)
        plt.plot(np.arange(0, len(R1[:i+1]), 1), R1[:i+1], 'b-')
        plt.plot(np.arange(0, len(R1[:i+1]), 1), np.zeros(len(R1[:i+1])) + 0.4, 'k--')
        plt.xlim([0, len(data1)])
        plt.ylim([-1.0, 1.0])
        plt.xlabel('Steps')
        plt.ylabel('Thermal Efficiency')

        plt.savefig('./champion_movie/champion_' + str(j) + '.png', dpi=300)
        plt.close()
        j += 1

os.system('ffmpeg -r 5 -i ./champion_movie/champion_%d.png -vcodec mpeg4 -y ./champion_movie/carnot.mp4')
