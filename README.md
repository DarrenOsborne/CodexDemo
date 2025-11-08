# Codex Demo Snake Game

This repository contains a tiny, intentionally plain-looking Snake game built with Python and [pygame](https://www.pygame.org/). It is meant to serve as a starting point for experimenting with Codex or other coding assistants—feel free to extend the visuals, add menus, sounds, or refactor the code base.

## Prerequisites

- Python 3.9 or newer (the game has been tested with Python 3.11)
- `pip` for installing Python packages

The only external dependency is `pygame`, which is listed in `requirements.txt`.

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/DarrenOsborne/CodexDemo.git
   cd codex-demo-snake
   ```

2. **Create (optional) and activate a virtual environment**

   ```bash
   python -m venv .venv
   # On Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game**

   ```bash
   python src/snake_game.py
   ```

   Use the arrow keys to guide the snake. Eating food increases your score and makes the snake longer. Colliding with yourself or the wall resets the game.

## Project Structure

```
.
├── README.md
├── requirements.txt
└── src
    ├── game_objects.py
    └── snake_game.py
```

- `snake_game.py` contains the game loop and rendering logic.
- `game_objects.py` defines the `Snake` and `Food` helper classes.

## Ideas for Improvements

- Make the graphics more interesting (textures, animations, particle effects, etc.).
- Add a start screen, pause functionality, or a scoreboard.
- Experiment with different board sizes or difficulty levels.
- Try refactoring the game into a class-based structure that separates rendering and game state even further.

Have fun experimenting!
