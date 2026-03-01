import pygame
from enum import Enum, auto

# main
SCREEN_MULTIPLIER: int = 4
SCREEN_CONSTANT: int = SCREEN_MULTIPLIER * 120
SIZE_CONSTANT: int = (SCREEN_MULTIPLIER - 1) * 10

# menu / button
BUTTON_SCALAR: int = SCREEN_MULTIPLIER - 1
MENU_MARGIN: int = BUTTON_SCALAR * 3

# camera
THRESHOLD_MULTIPLIER: int = 3
EASING_MULTIPLIER: int = 2

# world
SCORE_OFFSET: int = -(THRESHOLD_MULTIPLIER - 1)

# environment
GROUND_HEIGHT_MULTIPLIER: int = THRESHOLD_MULTIPLIER * 2
GROUND_START_MULTIPLIER: int = THRESHOLD_MULTIPLIER
WATER_GRID_SPACING_MULTIPLIER: int = 2
WATER_STARTING_ROW_ID: int = THRESHOLD_MULTIPLIER - 1

# log
MAX_SPEED_MULTIPLIER: int = 5
LOG_STARTING_ROW_ID: int = THRESHOLD_MULTIPLIER + 1
BORDER_RADIUS: int = SIZE_CONSTANT // 3

# player
SIZE_DECREASE_CONSTANT: int = 5
RECT_SIZE_DECREASE: float = 1 / SIZE_DECREASE_CONSTANT
MARGIN_DECREASE: float = (SIZE_DECREASE_CONSTANT * 2 - 1) / (SIZE_DECREASE_CONSTANT * 2)

# screen
SCREEN_MARGIN: int = 100
FPS: int = 120

# image
IMAGE_PATH: str = "assets/images/"
IMAGE_SCALE_CONSTANT: int = 20

# music
MUSIC_PATH: str = "assets/audio/"


# color palette
class ColorPalette:
    MAHOGANY: pygame.typing.ColorLike = "#4a3337"
    WATER: pygame.typing.ColorLike = "#6a8a99"
    GROUND: pygame.typing.ColorLike = "#4e6e60"
    FROG: pygame.typing.ColorLike = "#81967e"
    SAND: pygame.typing.ColorLike = "#ccbb98"
    ALPHA_SAND: pygame.typing.ColorLike = (204, 187, 152, 150)

    DEFAULT: pygame.typing.ColorLike = "#000000"
    FPS: pygame.typing.ColorLike = "#22ff00"


# game state
class GameState(Enum):
    MAIN_MENU = auto()
    PLAY = auto()
    QUIT = auto()
    SETTINGS = auto()
    PAUSE = auto()


# fonts
class Font: ...
