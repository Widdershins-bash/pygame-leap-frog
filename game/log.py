import pygame
import random

# TODO check the last log spawned in every row (for all 48 rows in this case (girth = 30)) and see if we can spawn a new log in that row


class Log:

    def __init__(self, surface: pygame.Surface, log_girth: int, rows: list[list[Log | None]]) -> None:
        self.surface: pygame.Surface = surface
        self.log_girth: int = log_girth
        self.log_rows: list[list[Log | None]] = rows

        self.start_y: int = self.surface.height - self.log_girth * 3
        self.x_pos, self.y_pos, self.log_length, self.speed = self.create_spawn()

    def create_spawn(self) -> tuple[float, int, int, int]:
        rand_row: int = random.randint(0, len(self.log_rows) - 1)
        speed: int = -(self.log_girth * 2) if rand_row % 2 == 1 else (self.log_girth * 2)

        length: int = random.randint(2, 4) * self.log_girth
        y_pos: int = self.start_y - rand_row * self.log_girth
        x_pos: float = 0 - length if speed > 0 else self.surface.width

        return (x_pos, y_pos, length, speed)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos, self.y_pos, self.log_length, self.log_girth)

    def draw(self):
        pygame.draw.rect(self.surface, "brown", self.get_rect(), 1, 5)

    def check_respawn(self) -> bool:
        res_point: int = self.surface.width if self.speed > 0 else 0 - self.log_length
        return (
            True
            if (self.x_pos > res_point and self.speed > 0) or (self.x_pos < res_point and self.speed < 0)
            else False
        )
