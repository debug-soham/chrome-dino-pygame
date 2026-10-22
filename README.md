# Chrome Dino Game (Pygame)

A clone of Chrome's offline dinosaur game, built only with Pygame. All graphics are drawn with simple shapes, so no image files are needed.

## Run

```bash
pip install pygame-ce
python main.py
```

## Controls

| Key | Action |
| --- | --- |
| `SPACE` / `UP` / `W` | Jump (also starts and restarts the game) |
| `DOWN` / `S` | Duck (or fall faster while in the air) |

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Entry point |
| `game.py` | Game loop, states (start / playing / game over), score, drawing |
| `dino.py` | Player: jumping, gravity, ducking, running animation |
| `obstacles.py` | Cactus, Bird and the manager that spawns them and checks collisions |
| `background.py` | Scrolling ground and clouds |
| `settings.py` | All constants: screen size, colors, physics, speed |

## How it works

- **Game loop**: every frame the game handles input, updates objects, then draws them (60 FPS).
- **Gravity**: the dino's vertical speed grows by `GRAVITY` each frame; a jump sets it to a negative value.
- **Speed**: the world speeds up a little every frame, up to `MAX_SPEED`.
- **Obstacles**: spawned on a random timer; birds appear after score 300.
- **Collision**: `pygame.Rect.colliderect` with a slightly shrunk hitbox to feel fair.
- **High score**: saved to `highscore.txt`.
