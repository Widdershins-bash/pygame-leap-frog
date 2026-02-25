import pygame

pygame.init()


class Image:

    def __init__(self, scalar: int) -> None:
        self.scalar: int = scalar
        self.img_path: str = "assets/images/"

    def button_sheet(self) -> pygame.Surface:
        button_sheet: pygame.Surface = pygame.image.load(self.img_path + "buttonsheet.png")
        button_sheet = pygame.transform.scale_by(button_sheet, self.scalar)
        return button_sheet
