import pygame
import random
import math
from PIL import Image
from abc import ABC, abstractmethod


class Snake:
    def __init__(self):
        self.color = (0, 255, 0)
        self.head_posx = None
        self.head_posy = None
        self.snakeList = []
        self.length = 1
        self.velocity = None
        self.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

    def draw_snake(self, display, block_size):
        for ele in self.snakeList:
            pygame.draw.rect(display, self.color, [ele[0], ele[1], block_size, block_size])

    # Dodajemy resztę węża jako listę, jeżeli nie zjadł żadnego jabłka, to reszta ciała będzie usuwana
    def snake_tail(self):
        tempList = []
        tempList.append(self.head_posx)
        tempList.append(self.head_posy)
        self.snakeList.append(tempList)
        if len(self.snakeList) > self.length:
            del self.snakeList[0]



class Object(ABC):
    @abstractmethod
    def draw_object(self, display, block_size):
        raise NotImplementedError('subclasses must override this function! (draw_object)')


class Apple(Object):
    def __init__(self, block_width, block_height, block_size):
        self.color = (255, 0, 0)
        self.posx = math.floor(random.randint(0, block_width - 1) * block_size)
        self.posy = math.floor(random.randint(0, block_height - 1) * block_size)

    def draw_object(self, display, block_size):
        pygame.draw.rect(display, self.color, [self.posx, self.posy, block_size, block_size])


class SpeedUp(Object):
    def __init__(self, block_width, block_height, block_size):
        self.color = (0, 0, 255)
        self.posx = math.floor(random.randint(0, block_width - 1) * block_size)
        self.posy = math.floor(random.randint(0, block_height - 1) * block_size)

    def draw_object(self, display, block_size):
        pygame.draw.rect(display, self.color, [self.posx, self.posy, block_size, block_size])


class Obstacle_static(Object):
    def __init__(self, block_width, block_height, block_size):
        self.color = (255, 255, 0)
        self.posx = math.floor(random.randint(0, block_width - 1) * block_size)
        self.posy = math.floor(random.randint(0, block_height - 1) * block_size)

    def draw_object(self, display, block_size):
        pygame.draw.rect(display, self.color, [self.posx, self.posy, block_size, block_size])


class Obstacle_moving(Snake):
    def __init__(self, block_size):
        super().__init__()
        self.color = (255, 0, 255)
        self.block_size = block_size
        self.velocity = 10
        self.length = 1



