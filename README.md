# 🐸 Leap Frog

Leap Frog is a small arcade-style Pygame project built around simple movement, reactive menus, and a clean grid-based world loop. The player hops across moving logs, avoids falling into water, and pushes upward to raise their score as the camera follows the action.

This project is structured like a compact game prototype, which makes it useful both as a playable experiment and as a portfolio piece showing game-loop organization, menu/state handling, asset management, collision systems, and modular Python code. 🎮

## ✨ Highlights

- Grid-based frog movement with upward scoring
- Moving log lanes with randomized speeds and counts
- Camera easing that follows player progress
- Main menu, pause menu, and settings UI
- Adjustable audio volume slider
- Lightweight asset pipeline for button sprites and sound effects
- Single-dependency setup with `pygame-ce`

## 🕹️ Controls

- `Space`: Jump forward / up one tile
- `Left Arrow`: Move left one tile
- `Right Arrow`: Move right one tile
- `F`: Toggle fullscreen
- `Esc`: Exit the game when not in fullscreen
- Mouse: Navigate menus and drag the volume slider

## 🧱 Tech Stack

- Python 3.12+ recommended
- [`pygame-ce`](https://pypi.org/project/pygame-ce/) `2.5.6`


## 🚀 Installation

### 1. Clone the repository

```powershell
git clone <your-repo-url>
cd LeapFrog
```

### 2. Create a virtual environment

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Game

With the virtual environment active:

```bash
python main.py
```

If `python` does not map to Python 3 on your machine, use:

```bash
python3 main.py
```

## 🔄 Pulling the Latest Changes

If you already cloned the project and want the newest version:

```powershell
git pull origin main
```

If your default branch is named something else, replace `main` with that branch name.

## 🧪 Development Notes

- The game currently depends on local assets under [`assets/`](./assets).
- Audio is loaded at runtime through `pygame.mixer.Sound`.
- Menus and gameplay share a single state-driven main loop.
- The project is lightweight and easy to extend with new obstacles, scoring rules, sprites, or movement behaviors.

## 🏗️ How the Game Works

At startup, `main.py` initializes Pygame, creates the screen, menu manager, world, and audio controller, then enters the main loop.

Inside that loop:

1. Delta time is calculated for smoother motion.
2. Input events are processed for quitting and fullscreen toggling.
3. The active game state determines whether gameplay updates should run.
4. The world updates logs, environment, player position, collisions, score, and camera offset.
5. Menus update and draw on top of the world as needed.
6. The logical surface is scaled to the window and presented to the player.

This separation makes the code easy to read and easy to grow. 🧠

## 🗂️ File-by-File Overview

#### `main.py`

Application entrypoint. Initializes Pygame, creates the screen, menu manager, sound system, and world, then runs the main game loop.

### `runtime/` modules

#### `runtime/constants.py`

Central configuration module for screen scaling, tile sizing, camera tuning, menu spacing, color palette values, asset paths, and the `GameState` enum.

#### `runtime/screen.py`

Owns the window, logical render surface, alpha overlay surface, fullscreen toggle logic, scaling-to-window behavior, FPS display, and tip text rendering.

#### `runtime/menu.py`

Implements menu orchestration. `MenuManager` switches between menus and widgets based on state, while `Menu` handles button updates, transitions, background drawing, and state returns.

#### `runtime/button.py`

Defines interactive UI components. Includes action buttons, the volume slider, slider knob behavior, hover/click state changes, and the button configuration used by menus.

#### `runtime/image.py`

Loads the button sprite sheet and slices it into reusable button surfaces such as play, quit, resume, settings, menu, volume, and knob sprites.

#### `runtime/music.py`

Loads and manages sound effects, tracks current audio volume, and synchronizes volume changes across UI and gameplay sounds.

### `game/` modules

#### `game/world.py`

Top-level gameplay coordinator. Updates environment, logs, player logic, collisions, score rendering, camera offset, and restart behavior.

#### `game/player.py`

Defines the frog/player behavior, including start position, tile movement, respawn logic, score increments, collision bounds, and rendering.

#### `game/log.py`

Implements the moving log system. Handles randomized lane generation, per-row movement, screen wrapping, collision checks, and log drawing.

#### `game/environment.py`

Defines environment objects like ground and water rows. The ground currently provides the main safe landing/collision zone, while water grid support is scaffolded for expansion.

#### `game/camera.py`

Provides a simple easing-based vertical camera offset so the world scrolls smoothly as the player advances upward.

### `assets/` folders

#### `assets/images/`

Stores UI image assets. The current game uses `buttonsheet.png` as the sprite source for buttons and the slider knob.

#### `assets/audio/`

Stores interface and gameplay sound effects such as clicks, swooshes, footsteps, grass sounds, and background-style audio assets.

## 🔮 Good Next Improvements

- Add upward and downward movement
- Add lose/win screens
- Introduce animated sprites for the frog and obstacles
- Add background music playback controls
- Persist volume settings between sessions
- Add high-score saving
- Add unit tests for camera math and collision helpers

## 🙌 Credits

Built with Python and Pygame Community Edition (`pygame-ce`).
