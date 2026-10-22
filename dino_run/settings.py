from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT_DIR / "assets" / "images"
HIGHSCORE_FILE = ROOT_DIR / "highscore.txt"

WIDTH, HEIGHT = 900, 350
FPS = 60
TITLE = "Dino Run"

GROUND_Y = 290

TEXT_COLOR = (60, 50, 60)
PANEL_COLOR = (255, 248, 235, 200)
DUST_COLOR = (250, 236, 205)

GRAVITY = 0.8
JUMP_SPEED = -15

START_SPEED = 7
SPEED_STEP = 0.002
MAX_SPEED = 18

BIRD_SCORE = 300
