import pygame
from .settings import WIDTH, TEXT_COLOR, PANEL_COLOR

GAME_OVER_COLOR = (200, 70, 60)


class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 20, bold=True)
        self.big_font = pygame.font.SysFont("consolas", 44, bold=True)

    def draw_text(self, screen, text, font, center, color=TEXT_COLOR):
        shadow = font.render(text, True, (255, 255, 255))
        screen.blit(shadow, shadow.get_rect(center=(center[0] + 2, center[1] + 2)))
        surface = font.render(text, True, color)
        screen.blit(surface, surface.get_rect(center=center))

    def draw_panel(self, screen, rect):
        panel = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, PANEL_COLOR, panel.get_rect(), border_radius=16)
        screen.blit(panel, rect)

    def draw_score(self, screen, score, high_score):
        text = f"HI {high_score:05d}   {score:05d}"
        surface = self.font.render(text, True, TEXT_COLOR)

        # Use only the visible pixels so the padding looks even on every side
        bounds = surface.get_bounding_rect()
        panel = pygame.Rect(0, 0, bounds.width + 32, bounds.height + 20)
        panel.topright = (WIDTH - 20, 18)
        self.draw_panel(screen, panel)
        screen.blit(surface, (panel.x + 16 - bounds.x, panel.y + 10 - bounds.y))

    def draw_title(self, screen, blink):
        cx = WIDTH // 2
        self.draw_text(screen, "DINO RUN", self.big_font, (cx, 110))
        if blink:
            self.draw_text(screen, "Press SPACE to start", self.font, (cx, 165))

    def draw_game_over(self, screen, score, new_best, blink):
        cx = WIDTH // 2
        self.draw_panel(screen, pygame.Rect(cx - 190, 60, 380, 160))
        self.draw_text(screen, "GAME OVER", self.big_font, (cx, 105), GAME_OVER_COLOR)
        label = "NEW BEST!  " if new_best else "SCORE  "
        self.draw_text(screen, f"{label}{score}", self.font, (cx, 150))
        if blink:
            self.draw_text(screen, "Press SPACE to restart", self.font, (cx, 190))
