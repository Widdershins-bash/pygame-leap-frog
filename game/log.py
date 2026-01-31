import pygame
import random


class Log:

    def __init__(self, surface: pygame.Surface, log_girth: int) -> None:
        self.surface: pygame.Surface = surface
        self.log_girth: int = log_girth

        self.max_unit_length: int = 6
        self.speed: int = random.randint(log_girth, log_girth * 5)
        self.y_pos, self.log_length = self.create_spawn()
        self.x_pos: float = surface.width

    def create_spawn(self) -> tuple[int, int]:
        random_y: int = (
            random.randint(
                -(self.log_girth // 10) * (self.surface.height // self.log_girth),
                (self.surface.height // self.log_girth),
            )
            * self.log_girth
        )
        random_length: int = random.randint(1, self.max_unit_length) * self.log_girth

        return (random_y, random_length)

    def draw(self):
        pygame.draw.rect(self.surface, "brown", pygame.Rect(self.x_pos, self.y_pos, self.log_length, self.log_girth))
