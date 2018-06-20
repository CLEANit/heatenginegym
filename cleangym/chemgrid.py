import numpy as np

class ChemGrid(object):
    def __init__(self, sizeX=5, sizeY=5, init_species=np.array([3, 3, 0])):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.init_species = init_species
        self.species = self.init_species

        self.species_map = {
               'A':0,
               'B':1,
               'C':2
        }

        self.num_species = len(self.species_map)

        self.reactions = {
               0: [self.species_map['A'], self.species_map['B'], self.species_map['C']]
        }

        self.recipes = {
               0: [1, 1, 1]
        }

        self.num_reactions = len(self.reactions)

        self.state = np.zeros((self.sizeX, self.sizeY, self.num_species), dtype = int)
        for i in range(self.num_species):
            for j in range(self.init_species[i]):
                placed = False
                while not placed:
                    X_pos = np.random.randint(0, self.sizeX)
                    Y_pos = np.random.randint(0, self.sizeY)
                    if self.state[X_pos, Y_pos].sum() == 0:
                        self.state[X_pos, Y_pos, i] = 1
                        placed = True

    def reset(self):
        self.state = np.zeros((self.sizeX, self.sizeY, self.num_species), dtype = int)
        for i in range(self.num_species):
            for j in range(self.init_species[i]):
                placed = False
                while not placed:
                    X_pos = np.random.randint(0, self.sizeX)
                    Y_pos = np.random.randint(0, self.sizeY)
                    if self.state[X_pos, Y_pos].sum() == 0:
                        self.state[X_pos, Y_pos, i] = 1
                        placed = True

    def move_N(self, X_pos, Y_pos):
        self.state = self.state

    def move_Up(self, X_pos, Y_pos):
        self.state[X_pos, (Y_pos + 1) % self.sizeY] += self.state[X_pos, Y_pos]
        self.state[X_pos, Y_pos] = np.zeros(self.num_species)

    def move_Down(self, X_pos, Y_pos):
        self.state[X_pos, (Y_pos - 1) % self.sizeY] += self.state[X_pos, Y_pos]
        self.state[X_pos, Y_pos] = np.zeros(self.num_species)

    def move_Left(self, X_pos, Y_pos):
        self.state[(X_pos - 1) % self.sizeX, Y_pos] += self.state[X_pos, Y_pos]
        self.state[X_pos, Y_pos] = np.zeros(self.num_species)

    def move_Right(self, X_pos, Y_pos):
        self.state[(X_pos + 1) % self.sizeX, Y_pos] += self.state[X_pos, Y_pos]
        self.state[X_pos, Y_pos] = np.zeros(self.num_species)

    def get_Truth(self, X_pos, Y_pos):
        for i in range(self.num_reactions):
            while self.state[X_pos, Y_pos, self.reactions[i][0]] >= self.recipes[i][0] and self.state[X_pos, Y_pos, self.reactions[i][1]] >= self.recipes[i][1]:
                self.state[X_pos, Y_pos, self.reactions[i][0]] -= self.recipes[i][0]
                self.species[self.reactions[i][0]] -= self.recipes[i][0]

                self.state[X_pos, Y_pos, self.reactions[i][1]] -= self.recipes[i][1]
                self.species[self.reactions[i][1]] -= self.recipes[i][1]

                self.state[X_pos, Y_pos, self.reactions[i][2]] += self.recipes[i][2]
                self.species[self.reactions[i][2]] += self.recipes[i][2]
