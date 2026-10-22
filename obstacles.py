import random
import pygame
from settings import WIDTH, GROUND_Y, FG_COLOR, START_SPEED, BIRD_SCORE


class Cactus:
    def __init__(self):
        count = random.randint(1, 3)
        self.width = 17 * count
        self.height = random.choice([35, 50])
        self.rect = pygame.Rect(WIDTH, GROUND_Y - self.height, self.width, self.height)
        self.count = count

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        for i in range(self.count):
            x = self.rect.x + i * 17
            pygame.draw.rect(screen, FG_COLOR, (x + 5, self.rect.y, 7, self.height))
            pygame.draw.rect(screen, FG_COLOR, (x, self.rect.y + 10, 4, 14))
            pygame.draw.rect(screen, FG_COLOR, (x + 13, self.rect.y + 6, 4, 14))


class Bird:
    HEIGHTS = [GROUND_Y - 30, GROUND_Y - 60, GROUND_Y - 95]

    def __init__(self):
        self.rect = pygame.Rect(WIDTH, random.choice(self.HEIGHTS), 42, 20)
        self.flap = 0

    def update(self, speed):
        self.rect.x -= speed + 1
        self.flap = (self.flap + 1) % 30

    def draw(self, screen):
        r = self.rect
        pygame.draw.rect(screen, FG_COLOR, (r.x + 8, r.y + 8, 30, 8))
        pygame.draw.rect(screen, FG_COLOR, (r.x, r.y + 6, 10, 6))
        wing_y = r.y - 4 if self.flap < 15 else r.y + 14
        pygame.draw.rect(screen, FG_COLOR, (r.x + 16, wing_y, 10, 10))


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

    def collides(self, rect):
        hitbox = rect.inflate(-10, -8)
        return any(hitbox.colliderect(o.rect) for o in self.items)

    def draw(self, screen):
        for obstacle in self.items:
            obstacle.draw(screen)
