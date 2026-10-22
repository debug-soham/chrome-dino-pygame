import os
import pygame
from settings import *
from dino import Dino
from obstacles import ObstacleManager
from background import Ground, Clouds


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20, bold=True)
        self.big_font = pygame.font.SysFont("consolas", 32, bold=True)
        self.high_score = self.load_high_score()
        self.state = "start"
        self.reset()

    def reset(self):
        self.dino = Dino()
        self.obstacles = ObstacleManager()
        self.ground = Ground()
        self.clouds = Clouds()
        self.speed = START_SPEED
        self.score = 0

    def load_high_score(self):
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE) as f:
                return int(f.read() or 0)
        return 0

    def save_high_score(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.high_score))

    def run(self):
        while True:
            self.handle_events()
            if self.state == "playing":
                self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                if self.state == "playing":
                    self.dino.jump()
                else:
                    self.reset()
                    self.state = "playing"
                    self.dino.jump()

    def update(self):
        keys = pygame.key.get_pressed()
        self.dino.update(keys)
        self.obstacles.update(self.speed, int(self.score))
        self.ground.update(self.speed)
        self.clouds.update()

        self.score += 0.15
        self.speed = min(self.speed + SPEED_STEP, MAX_SPEED)

        if self.obstacles.collides(self.dino.rect):
            self.state = "game_over"
            if int(self.score) > self.high_score:
                self.high_score = int(self.score)
                self.save_high_score()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.clouds.draw(self.screen)
        self.ground.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.dino.draw(self.screen)
        self.draw_score()

        if self.state == "start":
            self.draw_center("Press SPACE to start")
        elif self.state == "game_over":
            self.draw_center("G A M E   O V E R", "Press SPACE to restart")

        pygame.display.flip()

    def draw_score(self):
        text = f"HI {self.high_score:05d}  {int(self.score):05d}"
        surface = self.font.render(text, True, FG_COLOR)
        self.screen.blit(surface, (WIDTH - surface.get_width() - 20, 20))

    def draw_center(self, title, subtitle=None):
        surface = self.big_font.render(title, True, FG_COLOR)
        self.screen.blit(surface, surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        if subtitle:
            sub = self.font.render(subtitle, True, FG_COLOR)
            self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
