import numpy as np

class Policy():
    def __init__(self, state, hidden_units, num_actions):
        self.state = state
        self.size_X = self.state.shape[0]
        self.size_Y = self.state.shape[1]
        self.hidden_units = hidden_units
        self.num_actions = num_actions
        self.win = 0
        self.W = []
        self.B = []

    def gen_random(self):
        w, b = layer(self.size_Y, self.hidden_units[0])
        self.W.append(w)
        self.B.append(b)

        for i in range(1, len(self.hidden_units)):
            w, b = layer(self.hidden_units[i-1], self.hidden_units[i])
            self.W.append(w)
            self.B.append(b)

        w, b = layer(self.hidden_units[-1], self.num_actions)
        self.W.append(w)
        self.B.append(b)

    def evaluate(self, state):
        X = np.reshape(state, (self.size_X, self.size_Y))
        Y = np.matmul(X, self.W[0]) + self.B[0]

        for i in range(1, len(self.W)):
            Y = np.matmul(Y, self.W[i]) + self.B[i]

        Y = np.sum(Y, 0)

        return np.argmax(Y)

def layer(num_in, num_out):
    w = np.random.normal(size = (num_in, num_out))
    b = np.random.normal(size = num_out)
    return w, b

