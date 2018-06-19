import numpy as np

class Engine(object):
    def __init__(self, xmin=0, xmax=10, ymin=0, ymax=10, increment=1):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.increment = increment
        
        self.reset()
        self.state = self.get_state() 

    def get_state(self):
        return np.array([self.x,self.y])

    def reset(self):
        self.x = np.random.randint(self.xmin, self.xmax)
        self.y = np.random.randint(self.ymin, self.ymax)

    def move_left(self):
        if self.x > self.xmin:
            self.x -= self.increment
        return self.get_state()

    def move_right(self):
        if self.x < self.xmax:
            self.x += self.increment
        return self.get_state()
    
    def move_down(self):
        if self.y > self.ymin:
            self.y -= self.increment
        return self.get_state()

    def move_up(self):
        if self.y < self.ymax:
            self.y += self.increment
        return self.get_state()

    def no_move(self):
        return self.get_state()
