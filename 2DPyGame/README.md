# Snake Arcade Prototype

This is a simple Snake-style arcade game built with Pygame.

## Requirements
- Python 3.14+
- Pygame

## Run
```bash
python3 snake_game.py
```

## Install Pygame
If Pygame is not already installed, use these commands:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi

pip install pygame
```

## Controls
- Arrow keys: move
- ESC: open pause menu
- R: restart
- Q: quit

## Gameplay
- Collect green food dots to score points.
- Avoid red mine dots and colliding with yourself.
- New food spawns every 3 seconds.
- New mines spawn every 5 to 10 seconds.
