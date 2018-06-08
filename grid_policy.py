import numpy as np

class Policy():
    def __init__(self, num_actions):
        self.temp_map = {102: 0, 119: 1, 144: 2, 162: 3, 188: 4, 213: 5, 228: 6, 247: 7, 258: 8, 271: 9, 300: 10, 314: 11, 348: 12, 355: 13, 363: 14, 381: 15, 393: 16, 412: 17, 421: 18, 430: 19, 476: 20, 500: 21, 552: 22, 580: 23, 605: 24, 624: 25, 655: 26, 702: 27, 755: 28, 793: 29, 877: 30, 921: 31, 1040: 32, 1259: 33, 1462: 34}
        self.vol_map = {2: 0, 4: 1, 6: 2, 8: 3, 10: 4}
        self.shape = [len(self.temp_map), len(self.vol_map)]
        self.size_X = self.shape[0]
        self.size_Y = self.shape[1]
        self.win = 0
        self.num_actions = num_actions
        self.policy = np.zeros((self.size_X, self.size_Y))

    def gen_random(self):
        self.policy = np.random.randint(0, self.num_actions, (self.size_X, self.size_Y))

    def gen_perfect(self):
        self.policy[self.temp_map[300], self.vol_map[10]] = 2
        self.policy[self.temp_map[300], self.vol_map[8]] = 2
        self.policy[self.temp_map[300], self.vol_map[6]] = 2
        self.policy[self.temp_map[300], self.vol_map[4]] = 3
        self.policy[self.temp_map[500], self.vol_map[6]] = 1
        self.policy[self.temp_map[412], self.vol_map[8]] = 1
        self.policy[self.temp_map[355], self.vol_map[10]] = 2

    def evaluate(self, state):
        Y = self.policy[self.temp_map[int(state[0])], self.vol_map[int(state[1]*10000.0)]]

        return Y
