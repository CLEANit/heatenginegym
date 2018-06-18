import numpy as np

class GridObjects(object):
    def __init__(self, sizeX=5, sizeY=5):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.heroA_X = np.random.randint(0, self.sizeX)
        self.heroA_Y = np.random.randint(0, self.sizeY)
        self.heroB_X = np.random.randint(0, self.sizeX)
        self.heroB_Y = np.random.randint(0, self.sizeY)

    def reset(self):
        self.heroA_X = np.random.randint(0, self.sizeX)
        self.heroA_Y = np.random.randint(0, self.sizeY)
        self.heroB_X = np.random.randint(0, self.sizeX)
        while self.heroA_X == self.heroB_X:
            self.heroB_X = np.random.randint(0, self.sizeX)

        self.heroB_Y = np.random.randint(0, self.sizeY)
        while self.heroA_Y == self.heroB_Y:
            self.heroB_Y = np.random.randint(0, self.sizeY)

        self.__update_state()

    def __update_state(self):
        self.state = np.zeros((self.sizeX, self.sizeY))
        self.state[self.heroA_X, self.heroA_Y] += 0.25
        self.state[self.heroB_X, self.heroB_Y] += 0.75

    def move_N(self):
        self.__update_state()

    def move_A_Up(self):
        self.heroA_Y = (self.heroA_Y + 1) % self.sizeY
        self.__update_state()

    def move_A_Down(self):
        self.heroA_Y = (self.heroA_Y - 1) % self.sizeY
        self.__update_state()

    def move_A_Left(self):
        self.heroA_X = (self.heroA_X - 1) % self.sizeX
        self.__update_state()

    def move_A_Right(self):
        self.heroA_X = (self.heroA_X + 1) % self.sizeX
        self.__update_state()

    def move_B_Up(self):
        self.heroB_Y = (self.heroB_Y + 1) % self.sizeY
        self.__update_state()

    def move_B_Down(self):
        self.heroB_Y = (self.heroB_Y - 1) % self.sizeY
        self.__update_state()

    def move_B_Left(self):
        self.heroB_X = (self.heroB_X - 1) % self.sizeX
        self.__update_state()

    def move_B_Right(self):
        self.heroB_X = (self.heroB_X + 1) % self.sizeX
        self.__update_state()

    def move_A_Up_B_Up(self):
        self.heroA_Y = (self.heroA_Y + 1) % self.sizeY
        self.heroB_Y = (self.heroB_Y + 1) % self.sizeY
        self.__update_state()

    def move_A_Up_B_Down(self):
        self.heroA_Y = (self.heroA_Y + 1) % self.sizeY
        self.heroB_Y = (self.heroB_Y - 1) % self.sizeY
        self.__update_state()

    def move_A_Up_B_Left(self):
        self.heroA_Y = (self.heroA_Y + 1) % self.sizeY
        self.heroB_X = (self.heroB_X - 1) % self.sizeX
        self.__update_state()

    def move_A_Up_B_Right(self):
        self.heroA_Y = (self.heroA_Y + 1) % self.sizeY
        self.heroB_X = (self.heroB_X + 1) % self.sizeX
        self.__update_state()

    def move_A_Down_B_Up(self):
        self.heroA_Y = (self.heroA_Y - 1) % self.sizeY
        self.heroB_Y = (self.heroB_Y + 1) % self.sizeY
        self.__update_state()

    def move_A_Down_B_Down(self):
        self.heroA_Y = (self.heroA_Y - 1) % self.sizeY
        self.heroB_Y = (self.heroB_Y - 1) % self.sizeY
        self.__update_state()

    def move_A_Down_B_Left(self):
        self.heroA_Y = (self.heroA_Y - 1) % self.sizeY
        self.heroB_X = (self.heroB_X - 1) % self.sizeX
        self.__update_state()

    def move_A_Down_B_Right(self):
        self.heroA_Y = (self.heroA_Y - 1) % self.sizeY
        self.heroB_X = (self.heroB_X + 1) % self.sizeX
        self.__update_state()

    def move_A_Left_B_Up(self):
        self.heroA_X = (self.heroA_X - 1) % self.sizeX
        self.heroB_Y = (self.heroB_Y + 1) % self.sizeY
        self.__update_state()

    def move_A_Left_B_Down(self):
        self.heroA_X = (self.heroA_Y - 1) % self.sizeX
        self.heroB_Y = (self.heroB_Y - 1) % self.sizeY
        self.__update_state()

    def move_A_Left_B_Left(self):
        self.heroA_X = (self.heroA_Y - 1) % self.sizeX
        self.heroB_X = (self.heroB_X - 1) % self.sizeX
        self.__update_state()

    def move_A_Left_B_Right(self):
        self.heroA_X = (self.heroA_Y - 1) % self.sizeX
        self.heroB_X = (self.heroB_X + 1) % self.sizeX
        self.__update_state()

    def move_A_Right_B_Up(self):
        self.heroA_X = (self.heroA_X + 1) % self.sizeX
        self.heroB_Y = (self.heroB_Y + 1) % self.sizeY
        self.__update_state()

    def move_A_Right_B_Down(self):
        self.heroA_X = (self.heroA_Y + 1) % self.sizeX
        self.heroB_Y = (self.heroB_Y - 1) % self.sizeY
        self.__update_state()

    def move_A_Right_B_Left(self):
        self.heroA_X = (self.heroA_Y + 1) % self.sizeX
        self.heroB_X = (self.heroB_X - 1) % self.sizeX
        self.__update_state()

    def move_A_Right_B_Right(self):
        self.heroA_X = (self.heroA_Y + 1) % self.sizeX
        self.heroB_X = (self.heroB_X + 1) % self.sizeX
        self.__update_state()

