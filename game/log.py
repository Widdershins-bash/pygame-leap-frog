import pygame
from game.player import Player


class LogRow:
    def __init__(self, surface: pygame.Surface, speed: int, log_count: int, girth: int, row: int) -> None:
        self.surface: pygame.Surface = surface
        self.speed: int = speed if speed != 0 else 20
        self.log_count: int = log_count
        self.girth: int = girth
        self.row: int = row

        self.log_length: int = self.surface.width // self.log_count - self.girth
        self.logs: list[Log] = []
        for i in range(self.log_count + 1):
            log: Log = Log(self.surface, self.girth, self.speed, self.log_length)
            log.x_pos = i * (self.log_length + self.girth)
            log.y_pos = self.surface.height - self.row * self.girth
            self.logs.append(log)

    def update(self, delta_time: float, player: Player) -> None:
        for log in self.logs:
            log.x_pos += self.speed * delta_time

            if log.get_rect().colliderect(player.get_rect()):
                if (
                    self.speed < 0
                    and player.x_pos > 0
                    or self.speed > 0
                    and player.x_pos < self.surface.width - player.size
                ):
                    player.x_pos = log.x_pos
            log.draw()


class Log:

    def __init__(self, surface: pygame.Surface, girth: int, speed: int, length: int) -> None:
        self.surface: pygame.Surface = surface
        self.girth: int = girth
        self.speed: int = speed
        self.length: int = length

        self.x_pos: float
        self.y_pos: float

    def check_respawn(self) -> None:
        if self.speed > 0 and self.x_pos > self.surface.width + self.girth:
            self.x_pos = 0 - self.length
        elif self.speed < 0 and self.x_pos < -self.length - self.girth:
            self.x_pos = self.surface.width

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos, self.y_pos, self.length, self.girth)

    def draw(self) -> None:
        self.check_respawn()
        pygame.draw.rect(self.surface, "brown", self.get_rect())
