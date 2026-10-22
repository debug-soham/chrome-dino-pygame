"""Generates the pixel-art PNGs in assets/images. Run from the project root: python -m tools.make_sprites"""
import math
import random
import pygame
from dino_run.settings import WIDTH, HEIGHT, GROUND_Y, IMAGE_DIR

SCALE = 2
OUTLINE = (38, 44, 52)

PALETTE = {
    "G": (94, 186, 90),     # dino green
    "L": (190, 232, 150),   # dino belly
    "W": (255, 255, 255),
    "K": (30, 30, 30),
    "C": (46, 139, 87),     # cactus
    "H": (120, 204, 128),   # cactus highlight
    "P": (196, 106, 70),    # bird body
    "B": (245, 190, 70),    # bird beak
    "S": (222, 232, 242),   # cloud shade
}

HEAD = [
    "............GGGGGGGG",
    "...........GGGGGGGGGG",
    "...........GGWKGGGGGG",
    "...........GGKKGGGGGG",
    "...........GGGGGGGGGG",
    "...........GGGGGGGGGG",
    "...........GGGGGGGGGG",
    "...........GGGGG",
    "...........GGGGGGGG",
]
BODY = [
    "G.........GGGGG",
    "G........GGGGGG",
    "GG......GGGGGGGGG",
    "GGG....GGGGGGGG.G",
    "GGGG..GGGGGGGLL",
    "GGGGGGGGGGGLLLL",
    ".GGGGGGGGGLLLLL",
    "..GGGGGGGGLLLL",
    "...GGGGGGGGLL",
    "....GGGGGGGG",
]
LEGS_STAND = [".....GGG..GGG", ".....GG....GG", ".....GG....GG", ".....GGG...GGG"]
LEGS_RUN1 = [".....GGG..GGG", ".....GG....GGGG", ".....GG", ".....GGG"]
LEGS_RUN2 = [".....GGG..GGG", "...GGGG....GG", "...........GG", "...........GGG"]
DEAD_HEAD = [row.replace("WK", "KW") if i == 2 else row.replace("KK", "WK") if i == 3 else row
             for i, row in enumerate(HEAD)]

DUCK_BODY = [
    "...................GGGGGGGGG",
    "G.......GGGGGGGGGGGGWKGGGGGG",
    "GG....GGGGGGGGGGGGGGKKGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    ".GGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "..GGGGGGGGGGGGGGGGGGGGG",
    "...GGGGGGGLLLLLLLGGGGGGGGGG",
    "....GGGGGGLLLLLLLGGGG..GG",
    ".....GGGGGGGGGGGGGG.....G",
]
DUCK_LEGS1 = ["......GGG...GGG", "......GG.....GGGG", "......GGG"]
DUCK_LEGS2 = ["......GGG...GGG", "....GGGG.....GG", ".............GGG"]

CACTUS_SMALL = [
    "....CCC....",
    "...CHCCC...",
    "...CHCCC...",
    ".C.CHCCC.C.",
    "CC.CHCCC.CC",
    "CC.CHCCC.CC",
    "CC.CHCCC.CC",
    "CCCCHCCCCCC",
    ".CCCHCCCCC.",
] + ["...CHCCC..."] * 8

CACTUS_LARGE = [
    ".....CCCC......",
    "....CHHCCC.....",
    "....CHCCCC.....",
    "....CHCCCC..CC.",
    ".CC.CHCCCC.CHCC",
    "CHCCCHCCCC.CHCC",
    "CHCCCHCCCC.CHCC",
    "CHCCCHCCCC.CHCC",
    "CHCCCHCCCCCCHCC",
    "CHCCCHCCCCCCCC.",
    ".CCCCHCCCCCCC..",
    "..CCCHCCCC.....",
] + ["....CHCCCC....."] * 12

BIRD_UP = [
    "........P",
    "........PP",
    "........PPP",
    "...PP...PPPP",
    "..PKPP..PPPPP",
    "BBBPPPPPPPPPPPP",
    "....PPPPPPPPPPPPPPP",
    ".......PPPPPPPPP",
    "", "", "", "",
]
BIRD_DOWN = [
    "", "", "",
    "...PP",
    "..PKPP",
    "BBBPPPPPPPPPPPP",
    "....PPPPPPPPPPPPPPP",
    ".......PPPPPPPPP",
    "........PPPP",
    "........PPP",
    "........PP",
    "........P",
]

CLOUD = [
    "........WWWW",
    "......WWWWWWWW",
    "...WWWWWWWWWWWWWW",
    ".WWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWW",
    ".SSSSSSSSSSSSSSSSSSSSS",
]


def grid_to_surface(rows, outline=True, scale=SCALE):
    width = max(len(r) for r in rows)
    grid = [[PALETTE.get(ch) for ch in row.ljust(width, ".")] for row in rows]

    if outline:
        grid = [[None] * (width + 2)] + [[None] + row + [None] for row in grid] + [[None] * (width + 2)]
        h, w = len(grid), len(grid[0])
        filled = {(x, y) for y in range(h) for x in range(w) if grid[y][x]}
        for y in range(h):
            for x in range(w):
                if grid[y][x] is None and any((x + dx, y + dy) in filled
                                              for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                    grid[y][x] = OUTLINE

    surface = pygame.Surface((len(grid[0]) * scale, len(grid) * scale), pygame.SRCALPHA)
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            if color:
                surface.fill(color, (x * scale, y * scale, scale, scale))
    return surface


def make_sky(width, height):
    top, bottom = (110, 185, 235), (255, 222, 180)
    surface = pygame.Surface((width, height))
    for y in range(height):
        t = y / height
        color = [int(a + (b - a) * t) for a, b in zip(top, bottom)]
        pygame.draw.line(surface, color, (0, y), (width, y))
    for radius, alpha in ((70, 40), (52, 70)):
        glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 240, 180, alpha), (radius, radius), radius)
        surface.blit(glow, (700 - radius, 90 - radius))
    pygame.draw.circle(surface, (255, 236, 150), (700, 90), 36)
    return surface


def make_hills(width, height, color, waves):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    points = [(0, height)]
    for x in range(0, width + 1, 4):
        y = sum(amp * math.sin(2 * math.pi * cycles * x / width + phase) for amp, cycles, phase in waves)
        points.append((x, height * 0.45 + y))
    points.append((width, height))
    pygame.draw.polygon(surface, color, points)
    return surface


def make_ground(width, height):
    surface = pygame.Surface((width, height))
    surface.fill((238, 200, 135))
    pygame.draw.rect(surface, (200, 150, 90), (0, 0, width, 4))
    pygame.draw.rect(surface, (250, 220, 160), (0, 4, width, 3))
    for _ in range(140):
        x, y = random.randrange(width), random.randint(10, height - 4)
        color = random.choice([(214, 170, 110), (226, 186, 125), (190, 145, 95)])
        size = random.choice([2, 2, 4, 6])
        for offset in (0, -width):
            pygame.draw.rect(surface, color, (x + offset, y, size, 2))
    return surface


def main():
    random.seed(7)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    images = {
        "dino_run1": grid_to_surface(HEAD + BODY + LEGS_RUN1),
        "dino_run2": grid_to_surface(HEAD + BODY + LEGS_RUN2),
        "dino_jump": grid_to_surface(HEAD + BODY + LEGS_STAND),
        "dino_dead": grid_to_surface(DEAD_HEAD + BODY + LEGS_STAND),
        "dino_duck1": grid_to_surface(DUCK_BODY + DUCK_LEGS1),
        "dino_duck2": grid_to_surface(DUCK_BODY + DUCK_LEGS2),
        "cactus_small": grid_to_surface(CACTUS_SMALL),
        "cactus_large": grid_to_surface(CACTUS_LARGE),
        "bird1": grid_to_surface(BIRD_UP),
        "bird2": grid_to_surface(BIRD_DOWN),
        "cloud": grid_to_surface(CLOUD, outline=False, scale=4),
        "sky": make_sky(WIDTH, HEIGHT),
        "hills_far": make_hills(WIDTH, 140, (236, 170, 130), [(22, 2, 0), (12, 5, 1.3)]),
        "hills_near": make_hills(WIDTH, 100, (214, 140, 100), [(16, 3, 0.5), (8, 7, 2.1)]),
        "ground": make_ground(WIDTH, HEIGHT - GROUND_Y),
    }
    for name, surface in images.items():
        pygame.image.save(surface, IMAGE_DIR / f"{name}.png")
    print(f"Saved {len(images)} images to {IMAGE_DIR}")


if __name__ == "__main__":
    main()
