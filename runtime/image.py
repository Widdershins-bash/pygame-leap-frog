import pygame
from runtime.constants import IMAGE_PATH, IMAGE_SCALE_CONSTANT


class ImageManager:
    def __init__(self, scalar: int) -> None:
        self.scalar: int = scalar
        self.path: str = IMAGE_PATH

        self.button: ButtonSprite = ButtonSprite(path=self.path, scalar=self.scalar)


class ButtonSprite:
    def __init__(self, path: str, scalar: int) -> None:
        self.path: str = path
        self.scalar: int = scalar

        self.sheet: pygame.Surface = self.sprite_sheet()

        self.x_scalar: int = IMAGE_SCALE_CONSTANT * 4 * self.scalar
        self.y_scalar: int = IMAGE_SCALE_CONSTANT * self.scalar

        self.play: pygame.Surface = self.sheet.subsurface((0, 0, self.x_scalar, self.y_scalar))
        self.quit: pygame.Surface = self.sheet.subsurface((0, self.y_scalar, self.x_scalar, self.y_scalar))
        self.resume: pygame.Surface = self.sheet.subsurface((0, 2 * self.y_scalar, self.x_scalar, self.y_scalar))
        self.menu: pygame.Surface = self.sheet.subsurface((0, 3 * self.y_scalar, self.x_scalar, self.y_scalar))
        self.volume: pygame.Surface = self.sheet.subsurface((0, 4 * self.y_scalar, self.x_scalar, self.y_scalar))
        self.knob: pygame.Surface = self.sheet.subsurface(
            (self.y_scalar, 5 * self.y_scalar, 6 * self.scalar, 6 * self.scalar)
        )
        self.settings: pygame.Surface = self.sheet.subsurface((0, 5 * self.y_scalar, self.y_scalar, self.y_scalar))

    def sprite_sheet(self) -> pygame.Surface:
        button_sheet: pygame.Surface = pygame.image.load(self.path + "buttonsheet.png")
        button_sheet = pygame.transform.scale_by(button_sheet, self.scalar)
        return button_sheet
