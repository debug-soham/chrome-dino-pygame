import random
import pygame
from .resources import load_image
from .settings import GROUND_Y, GRAVITY, JUMP_SPEED, DUST_COLOR


class Dust:
    """Small puffs of sand kicked up behind the dino."""

    def __init__(self):
        self.particles = []

    def emit(self, x, y, amount=1):
        for _ in range(amount):
            # [x, y, x speed, y speed, size]
            self.particles.append([x, y, random.uniform(-1, 0), random.uniform(-1.5, -0.3), random.uniform(3, 6)])

    def update(self, speed):
        for p in self.particles:
            p[0] += p[2] - speed * 0.5
            p[1] += p[3]
            p[4] -= 0.15
        self.particles = [p for p in self.particles if p[4] > 0]

    def draw(self, screen):
        for x, y, _, _, size in self.particles:
            pygame.draw.circle(screen, DUST_COLOR, (int(x), int(y)), int(size))


class Dino:
    def __init__(self):
        self.run_frames = [load_image("dino_run1"), load_image("dino_run2")]
        self.duck_frames = [load_image("dino_duck1"), load_image("dino_duck2")]
        self.jump_image = load_image("dino_jump")
        self.dead_image = load_image("dino_dead")
        self.dust = Dust()

        self.x = 60
        self.y = GROUND_Y
        self.vel_y = 0
        self.ducking = False
        self.dead = False
        self.step = 0

    @property
    def on_ground(self):
        return self.y >= GROUND_Y

    @property
    def image(self):
        if self.dead:
            return self.dead_image
        if not self.on_ground:
            return self.jump_image
        frames = self.duck_frames if self.ducking else self.run_frames
        return frames[self.step // 6 % 2]

    @property
    def rect(self):
        # self.y is the dino's feet, so every frame stands on the ground
        return self.image.get_rect(bottomleft=(self.x, self.y + 4))

    @property
    def mask(self):
        return pygame.mask.from_surface(self.image)

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_SPEED

    def update(self, keys, speed):
        was_on_ground = self.on_ground
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.ducking = down and self.on_ground

        # Holding down mid-air makes the dino fall faster
        fall_boost = 2 if down and not self.on_ground else 1
        self.vel_y += GRAVITY * fall_boost
        self.y = min(self.y + self.vel_y, GROUND_Y)
        if self.on_ground:
            self.vel_y = 0

        feet = (self.x + 10, GROUND_Y)
        if self.on_ground and not was_on_ground:
            self.dust.emit(*feet, amount=8)
        elif self.on_ground and self.step % 4 == 0:
            self.dust.emit(*feet)
        self.dust.update(speed)

        self.step += 1

    def draw(self, screen):
        self.dust.draw(screen)
        screen.blit(self.image, self.rect)
