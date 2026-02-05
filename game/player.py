import pygame

pygame.init()


class Player:

    def __init__(self, surface: pygame.Surface, size: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = size

        self.speed_offset: int = 0
        self.x_pos, self.y_pos = self.start_pos()
        self.margin: int = self.size // 10

    def start_pos(self) -> tuple[float, float]:
        x: float = (self.surface.width - self.size) // 2
        y: float = self.surface.height - self.size
        return (x, y)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)

    def draw(self):
        pygame.draw.rect(self.surface, "green", self.get_rect(), border_radius=self.size // 2)
