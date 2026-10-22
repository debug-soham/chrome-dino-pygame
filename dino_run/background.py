import random
from .resources import load_image
from .settings import WIDTH, GROUND_Y


class Layer:
    """An image that scrolls left and repeats, slower for things far away."""

    def __init__(self, name, y, depth):
        self.image = load_image(name)
        self.y = y
        self.depth = depth
        self.offset = 0

    def update(self, speed):
        self.offset = (self.offset + speed * self.depth) % WIDTH

    def draw(self, screen):
        screen.blit(self.image, (-self.offset, self.y))
        screen.blit(self.image, (WIDTH - self.offset, self.y))


class Clouds:
    def __init__(self):
        self.image = load_image("cloud")
        self.items = [[random.randint(0, WIDTH), random.randint(30, 140)] for _ in range(4)]

    def update(self):
        for cloud in self.items:
            cloud[0] -= 0.6
            if cloud[0] < -self.image.get_width():
                cloud[0] = WIDTH + random.randint(0, 200)
                cloud[1] = random.randint(30, 140)

    def draw(self, screen):
        for x, y in self.items:
            screen.blit(self.image, (x, y))


class Background:
    def __init__(self):
        self.sky = load_image("sky")
        self.clouds = Clouds()
        self.layers = [
            Layer("hills_far", GROUND_Y - 140, 0.1),
            Layer("hills_near", GROUND_Y - 100, 0.3),
            Layer("ground", GROUND_Y, 1),
        ]

    def update(self, speed):
        self.clouds.update()
        for layer in self.layers:
            layer.update(speed)

    def draw(self, screen):
        screen.blit(self.sky, (0, 0))
        self.clouds.draw(screen)
        for layer in self.layers:
            layer.draw(screen)
