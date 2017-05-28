import arcade as ar
import numpy as np
import random


class Brain:
    def __init__(self):
        pass

    def decide(self, input_data):
        pass


class Dumb(Brain):
    def __init__(self, dir):
        self.dir = dir
        super().__init__()

    def decide(self, input_data):
        return self.dir


class User(Brain):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.last = [0, 1]

    def decide(self, input_data):
        if self.game.buttons[ar.key.UP]:
            self.last = [0, 1]
            return [0, 1]
        elif self.game.buttons[ar.key.RIGHT]:
            self.last = [1, 0]
            return [1, 0]
        elif self.game.buttons[ar.key.DOWN]:
            self.last = [0, -1]
            return [0, -1]
        elif self.game.buttons[ar.key.LEFT]:
            self.last = [-1, 0]
            return [-1, 0]
        else:
            return self.last


class NN(Brain):
    def __init__(self, game, W1=None, W2=None):
        super().__init__()
        self.game = game
        if W1 is None or W2 is None:
            self.W = (np.random.rand(4, 9) - 0.5) * 2
        else:
            net = np.random.rand(*W1.shape) > 0.5
            self.W = W1 * net + W2 * np.logical_not(net) - 1
            if random.random() > 0.6:
                self.mutate()

    def decide(self, input_data):
        answer = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        x = np.concatenate((np.array([1]), input_data))
        y = x.dot(self.W.T)
        return answer[list(y).index(np.max(y))]

    def mutate(self):
        random_W = ((np.random.rand(4, 9)) * 3).astype("int8")-1
        net = np.random.rand(*self.W.shape) > 0.3
        self.W = net * self.W + np.logical_not(net) * (random_W*0.6 + self.W*0.4)
        negating_net = np.ones(self.W.shape) - (np.random.rand(*self.W.shape) > 0.95) * 2
        self.W = self.W * negating_net
