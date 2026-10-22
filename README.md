# Dino Run (Pygame)

A clone of Chrome's offline dinosaur game, built only with Pygame. It has pixel-art sprites, a desert scene with parallax hills, dust effects, and pixel-perfect collisions.

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

```
main.py                 Entry point
dino_run/               The game package
  game.py               Game loop and states (start / playing / game over)
  dino.py               Player: jumping, gravity, ducking, animation, dust puffs
  obstacles.py          Cactus, Bird and the manager that spawns them and checks collisions
  background.py         Sky, clouds and scrolling parallax layers (hills, ground)
  ui.py                 Score box, title screen and game-over panel
  resources.py          Loads images (each one only once) and saves the high score
  settings.py           All constants: paths, screen size, colors, physics, speed
assets/images/          PNG sprites used by the game
tools/make_sprites.py   Script that draws the PNG sprites from text pixel grids
```

## How it works

- **Game loop**: every frame the game handles input, updates objects, then draws them (60 FPS).
- **Gravity**: the dino's vertical speed grows by `GRAVITY` each frame; a jump sets it to a negative value.
- **Animation**: the dino and bird switch between two images every few frames.
- **Parallax**: background layers move at different speeds (far hills slow, ground fast) to create depth.
- **Speed**: the world speeds up a little every frame, up to `MAX_SPEED`.
- **Obstacles**: spawned on a random timer; birds appear after score 300.
- **Collision**: `pygame.mask` compares the actual pixels of the dino and obstacles, so transparent corners don't count.
- **High score**: saved to `highscore.txt`.

## Sprites

All images are original pixel art, drawn by `tools/make_sprites.py` from small text grids (each letter is a color). To change a sprite, edit its grid and run this from the project root:

```bash
python -m tools.make_sprites
```
