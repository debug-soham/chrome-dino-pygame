import random
import pygame
from .resources import load_image
from .settings import WIDTH, GROUND_Y, START_SPEED, BIRD_SCORE


class Obstacle:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(image)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Cactus(Obstacle):
    def __init__(self):
        part = load_image(random.choice(["cactus_small", "cactus_large"]))
        count = random.randint(1, 3)
        step = part.get_width() - 6

        # Join 1-3 cacti side by side into one image
        group = pygame.Surface((step * (count - 1) + part.get_width(), part.get_height()), pygame.SRCALPHA)
        for i in range(count):
            group.blit(part, (i * step, 0))
        super().__init__(group, WIDTH, GROUND_Y - group.get_height() + 4)


class Bird(Obstacle):
    HEIGHTS = [GROUND_Y - 40, GROUND_Y - 72, GROUND_Y - 110]

    def __init__(self):
        self.frames = [load_image("bird1"), load_image("bird2")]
        self.flap = 0
        super().__init__(self.frames[0], WIDTH, random.choice(self.HEIGHTS))

    def update(self, speed):
        super().update(speed + 1)
        self.flap += 1
        self.image = self.frames[self.flap // 12 % 2]
        self.mask = pygame.mask.from_surface(self.image)


class ObstacleManager:
    def __init__(self):
        self.items = []
        self.timer = 0

    def update(self, speed, score):
        self.timer -= 1
        if self.timer <= 0:
            self.spawn(score)
            self.timer = random.randint(55, 110) * START_SPEED / speed

        for obstacle in self.items:
            obstacle.update(speed)
        self.items = [o for o in self.items if o.rect.right > 0]

    def spawn(self, score):
        if score > BIRD_SCORE and random.random() < 0.3:
            self.items.append(Bird())
        else:
            self.items.append(Cactus())

    def collides(self, dino):
        # Pixel-perfect check: only solid pixels count, not the empty corners
        for o in self.items:
            offset = (o.rect.x - dino.rect.x, o.rect.y - dino.rect.y)
            if dino.mask.overlap(o.mask, offset):
                return True
        return False

    def draw(self, screen):
        for obstacle in self.items:
            obstacle.draw(screen)
