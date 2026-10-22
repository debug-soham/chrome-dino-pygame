import pygame
from settings import GROUND_Y, GRAVITY, JUMP_SPEED, FG_COLOR, BG_COLOR


class Dino:
    RUN_SIZE = (44, 47)
    DUCK_SIZE = (59, 30)

    def __init__(self):
        self.x = 60
        self.y = GROUND_Y - self.RUN_SIZE[1]
        self.vel_y = 0
        self.ducking = False
        self.step = 0

    @property
    def on_ground(self):
        return self.rect.bottom >= GROUND_Y

    @property
    def rect(self):
        w, h = self.DUCK_SIZE if self.ducking else self.RUN_SIZE
        return pygame.Rect(self.x, self.y + self.RUN_SIZE[1] - h, w, h)

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_SPEED

    def update(self, keys):
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.ducking = down and self.on_ground

        # Holding down mid-air makes the dino fall faster
        fall_boost = 2 if down and not self.on_ground else 1
        self.vel_y += GRAVITY * fall_boost
        self.y += self.vel_y

        if self.y + self.RUN_SIZE[1] >= GROUND_Y:
            self.y = GROUND_Y - self.RUN_SIZE[1]
            self.vel_y = 0

        self.step = (self.step + 1) % 20

    def draw(self, screen):
        r = self.rect
        if self.ducking:
            pygame.draw.rect(screen, FG_COLOR, (r.x, r.y + 6, r.w - 14, r.h - 14))
            pygame.draw.rect(screen, FG_COLOR, (r.right - 22, r.y, 22, 16))
            pygame.draw.rect(screen, BG_COLOR, (r.right - 14, r.y + 4, 4, 4))
        else:
            pygame.draw.rect(screen, FG_COLOR, (r.x + 20, r.y, 24, 18))
            pygame.draw.rect(screen, BG_COLOR, (r.x + 26, r.y + 4, 4, 4))
            pygame.draw.rect(screen, FG_COLOR, (r.x + 6, r.y + 16, 26, 20))
            pygame.draw.rect(screen, FG_COLOR, (r.x, r.y + 14, 8, 14))
            pygame.draw.rect(screen, FG_COLOR, (r.x + 32, r.y + 22, 8, 4))
        self._draw_legs(screen, r)

    def _draw_legs(self, screen, r):
        legs_y = r.bottom - 11
        if not self.on_ground:
            left, right = 11, 11
        elif self.step < 10:
            left, right = 11, 6
        else:
            left, right = 6, 11
        pygame.draw.rect(screen, FG_COLOR, (r.x + 10, legs_y, 5, left))
        pygame.draw.rect(screen, FG_COLOR, (r.x + 22, legs_y, 5, right))
