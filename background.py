import random
import pygame
from settings import WIDTH, GROUND_Y, FG_COLOR, CLOUD_COLOR


class Ground:
    def __init__(self):
        self.offset = 0
        self.bumps = [(random.randint(0, WIDTH), random.randint(4, 12)) for _ in range(30)]

    def update(self, speed):
        self.offset = (self.offset + speed) % WIDTH

    def draw(self, screen):
        pygame.draw.line(screen, FG_COLOR, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        for x, y in self.bumps:
            bx = (x - self.offset) % WIDTH
            pygame.draw.line(screen, FG_COLOR, (bx, GROUND_Y + y), (bx + 3, GROUND_Y + y))


class Clouds:
    def __init__(self):
        self.items = [[random.randint(0, WIDTH), random.randint(40, 130)] for _ in range(3)]

    def update(self):
        for cloud in self.items:
            cloud[0] -= 1
            if cloud[0] < -60:
                cloud[0] = WIDTH + random.randint(0, 200)
                cloud[1] = random.randint(40, 130)

    def draw(self, screen):
        for x, y in self.items:
            pygame.draw.ellipse(screen, CLOUD_COLOR, (x, y, 60, 18))
            pygame.draw.ellipse(screen, CLOUD_COLOR, (x + 15, y - 8, 30, 18))
