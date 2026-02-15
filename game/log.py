import pygame
from game.player import Player
from random import randint


class LogRow:
    def __init__(self, surface: pygame.Surface, speed: int, log_count: int, girth: int, row: int) -> None:
        self.surface: pygame.Surface = surface
        self.speed: int = speed if speed != 0 else 20
        self.log_count: int = log_count
        self.girth: int = girth
        self.row: int = row

        self.screen_segments: int = self.surface.width // self.girth
        self.segment_space: int = self.screen_segments // self.log_count - 1

        self.logs: list[Log] = []
        for i in range(self.log_count + 1):
            log_segments: int = self.segment_space - randint(1, 2) if self.segment_space > 2 else self.segment_space
            log: Log = Log(surface=self.surface, girth=self.girth, speed=self.speed, segments=log_segments)
            log.x_pos = i * (self.segment_space * self.girth + self.girth)
            log.y_pos = self.surface.height - self.row * self.girth
            self.logs.append(log)

    def update(self, delta_time: float, player: Player) -> None:
        for log in self.logs:
            log.x_pos += self.speed * delta_time
            if log.check_player_collision(player=player):
                log.set_player_pos(player=player)
                player.splashed = False
            log.check_respawn()
            log.draw()


class Log:

    def __init__(self, surface: pygame.Surface, girth: int, speed: int, segments: int) -> None:
        self.surface: pygame.Surface = surface
        self.girth: int = girth
        self.speed: int = speed
        self.segments: int = segments

        self.x_pos: float
        self.y_pos: float

    def check_respawn(self) -> None:
        if self.speed > 0 and self.x_pos > self.surface.width + self.girth:
            self.x_pos = 0 - self.segments * self.girth
        elif self.speed < 0 and self.x_pos < -self.girth - self.segments * self.girth:
            self.x_pos = self.surface.width

    def check_player_collision(self, player: Player) -> bool:
        return self.get_rect().colliderect(player.get_rect())

    def set_player_pos(self, player: Player) -> None:
        if self.speed < 0 and player.x_pos > 0 or self.speed > 0 and player.x_pos < self.surface.width - player.size:
            relative_seg_pos: list[int] = [
                abs((int(self.x_pos) + i * player.size) - int(player.x_pos)) for i in range(self.segments)
            ]
            closest_seg: int = min(relative_seg_pos)
            player.x_pos = self.x_pos + relative_seg_pos.index(closest_seg) * player.size

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos, self.y_pos, self.girth * self.segments, self.girth)

    def draw(self) -> None:
        pygame.draw.rect(self.surface, "brown", self.get_rect())
