import pygame

pygame.init()


class Player:

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface: pygame.Surface = surface
        self.x_pos: int = 0
        self.y_pos: int = 0
        self.sprite: pygame.Rect = pygame.Rect(self.x_pos, self.y_pos, 100, 100)

    def draw(self):
        pygame.draw.rect(self.surface, "black", self.sprite)
