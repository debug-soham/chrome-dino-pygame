import pygame
from .settings import WIDTH, HEIGHT, FPS, TITLE, START_SPEED, SPEED_STEP, MAX_SPEED
from .dino import Dino
from .obstacles import ObstacleManager
from .background import Background
from .ui import UI
from .resources import load_high_score, save_high_score

JUMP_KEYS = (pygame.K_SPACE, pygame.K_UP, pygame.K_w)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.high_score = load_high_score()
        self.state = "start"
        self.frame = 0
        self.reset()

    def reset(self):
        self.dino = Dino()
        self.obstacles = ObstacleManager()
        self.background = Background()
        self.speed = START_SPEED
        self.score = 0
        self.new_best = False

    def run(self):
        while True:
            self.handle_events()
            if self.state == "playing":
                self.update()
            self.draw()
            self.frame += 1
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key in JUMP_KEYS:
                if self.state != "playing":
                    self.reset()
                    self.state = "playing"
                self.dino.jump()

    def update(self):
        self.dino.update(pygame.key.get_pressed(), self.speed)
        self.obstacles.update(self.speed, int(self.score))
        self.background.update(self.speed)

        self.score += 0.15
        self.speed = min(self.speed + SPEED_STEP, MAX_SPEED)

        if self.obstacles.collides(self.dino):
            self.game_over()

    def game_over(self):
        self.state = "game_over"
        self.dino.dead = True
        if int(self.score) > self.high_score:
            self.high_score = int(self.score)
            self.new_best = True
            save_high_score(self.high_score)

    def draw(self):
        self.background.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.dino.draw(self.screen)
        self.ui.draw_score(self.screen, int(self.score), self.high_score)

        blink = self.frame // 30 % 2 == 0
        if self.state == "start":
            self.ui.draw_title(self.screen, blink)
        elif self.state == "game_over":
            self.ui.draw_game_over(self.screen, int(self.score), self.new_best, blink)

        pygame.display.flip()
