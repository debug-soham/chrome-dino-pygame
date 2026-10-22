from functools import cache
import pygame
from .settings import IMAGE_DIR, HIGHSCORE_FILE


@cache
def load_image(name):
    return pygame.image.load(IMAGE_DIR / f"{name}.png").convert_alpha()


def load_high_score():
    if HIGHSCORE_FILE.exists():
        return int(HIGHSCORE_FILE.read_text() or 0)
    return 0


def save_high_score(score):
    HIGHSCORE_FILE.write_text(str(score))
