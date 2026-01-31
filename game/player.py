import pygame

pygame.init()


class Player:

    def __init__(self, surface: pygame.Surface, size: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = size
        self.x_pos: int
        self.y_pos: int
        self.sprite: pygame.Rect
        self.jumped: bool = False

    def draw(self, pos: tuple[int, int]):
        self.x_pos, self.y_pos = pos
        self.sprite = pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)
        pygame.draw.rect(self.surface, "green", self.sprite, border_radius=self.size // 3)
