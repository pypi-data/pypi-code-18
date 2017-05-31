from config import *
import arcade as ar
import numpy as np
import random
from collections import deque
import math


class BodySegment:
    def __init__(self, color, pos, head=False):
        self.pos = pos
        self.color = color
        self.head = head

    def move(self, dir):
        self.pos[0] += dir[0]
        self.pos[0] %= MAP_WIDTH

        self.pos[1] += dir[1]
        self.pos[1] %= MAP_HEIGHT

    def update(self):
        pass

    def draw(self):
        drawing_pos = (self.pos[0] * RECT_WIDTH + RECT_WIDTH//2, self.pos[1] * RECT_HEIGHT + RECT_HEIGHT//2+1)
        ar.draw_rectangle_filled(*drawing_pos, RECT_WIDTH - GAP, RECT_HEIGHT - GAP, self.color)
        if self.head:
            ar.draw_rectangle_filled(*drawing_pos, (RECT_WIDTH-GAP)//2, (RECT_HEIGHT-GAP)//2, (np.array(self.color)*0.3).astype("int8"))
            ar.draw_rectangle_outline(*drawing_pos, (RECT_WIDTH-GAP)//2, (RECT_HEIGHT-GAP)//2, WHITE, 2)

    def lays_on(self, pos):
        return pos[0] == self.pos[0] and pos[1] == self.pos[1]


class Snake:
    def __init__(self, pos, game, brain, id):
        self.id = id
        self.game = game
        self.color = random.choice(COLORS)
        self.body = [BodySegment(self.color, pos, head=True)]
        self.history = deque([])
        self.brain = brain
        self.timer = max(MAP_HEIGHT,MAP_WIDTH)*TIMER_RATIO
        self.time_left = self.timer
        self.ticks = 0
        self.longest = 1

    def move(self):
        left = MAP_WIDTH
        right = MAP_WIDTH
        down = MAP_HEIGHT
        up = MAP_HEIGHT

        for snake_id in self.game.snakes:
            snake = self.game.snakes[snake_id]
            for seg in snake.body:
                diff_x = abs(seg.pos[0] - self.body[0].pos[0])
                diff_y = abs(seg.pos[1] - self.body[0].pos[1])
                if diff_x + diff_y == 0:
                    pass
                elif diff_y == 0:
                    if seg.pos[0] < self.body[0].pos[0]:
                        left = min(diff_x, left)
                        right = min(MAP_WIDTH - diff_x, right)
                    else:
                        right = min(diff_x, right)
                        left = min(MAP_WIDTH - diff_x, left)

                elif diff_x == 0:
                    if seg.pos[1] < self.body[0].pos[1]:
                        down = min(diff_y, down)
                        up = min(MAP_HEIGHT - diff_y, up)
                    else:
                        up = min(diff_y, up)
                        down = min(MAP_HEIGHT - diff_y, down)

        input_snakes = (np.array([MAP_HEIGHT, MAP_WIDTH, MAP_HEIGHT, MAP_WIDTH]) - np.array([up, right, down, left]))**10/np.array([MAP_HEIGHT-1, MAP_WIDTH-1, MAP_HEIGHT-1, MAP_WIDTH-1])**10

        left = MAP_WIDTH
        right = MAP_WIDTH
        down = MAP_HEIGHT
        up = MAP_HEIGHT
        for apple in self.game.apples:
            diff_x = abs(apple.pos[0] - self.body[0].pos[0])
            diff_y = abs(apple.pos[1] - self.body[0].pos[1])
            if diff_y == 0:
                if apple.pos[0] < self.body[0].pos[0]:
                    left = min(diff_x, left)
                    right = min(MAP_WIDTH - diff_x, right)
                else:
                    right = min(diff_x, right)
                    left = min(MAP_WIDTH - diff_x, left)

            elif diff_x == 0:
                if apple.pos[1] < self.body[0].pos[1]:
                    down = min(diff_y, down)
                    up = min(MAP_HEIGHT - diff_y, up)
                else:
                    up = min(diff_y, up)
                    down = min(MAP_HEIGHT - diff_y, down)

        input_apple = (np.array([MAP_HEIGHT, MAP_WIDTH, MAP_HEIGHT, MAP_WIDTH]) - np.array([up, right, down, left]))**2/np.array([MAP_HEIGHT-1, MAP_WIDTH-1, MAP_HEIGHT-1, MAP_WIDTH-1])**2
        dir = self.brain.decide(np.concatenate((input_snakes, input_apple)))

        for snake_id in self.game.snakes:
            if self.game.snakes[snake_id].lays_on([self.body[0].pos[0] + dir[0], self.body[0].pos[1] + dir[1]]):
                self.die()
                return

        self.history.appendleft(dir)
        last_pos = self.body[-1].pos.copy()

        for i in range(len(self.body)):
            self.body[i].move(self.history[i])
        for i in range(len(self.game.apples)):
            if self.game.apples[i].lays_on(self.body[0].pos):
                self.body.append(BodySegment(self.color, last_pos))
                self.game.apples[i].eat()
                if len(self.body)>self.longest:
                    self.longest = len(self.body)

        if len(self.history) >= len(self.body):
            self.history.pop()

        self.time_left -= 1
        self.ticks += 1
        if self.time_left < 1:
            self.time_left += self.timer
            del self.body[-1]
            if len(self.body) == 0:
                self.die()
                return

    def update(self):
        pass

    def draw(self):
        for segment in self.body:
            segment.draw()

    def lays_on(self, pos):
        for seg in self.body:
            if seg.lays_on(pos):
                return True
        return False

    def die(self):
        self.game.snake_died(self.id)


class Apple(BodySegment):
    def __init__(self, game):
        self.game = game
        super().__init__(RED, [0, 0])
        self.grow()

    def grow(self):
        self.pos = self.game.get_free_place()

    def eat(self):
        self.grow()
