import pygame
from game.player import Player
from game.log import LogSystem
from game.camera import Camera


class World:
    def __init__(self) -> None:
        self.player: Player = 

    def set_onlog(self, log: Log) -> None:
        if (log.speed < 0 and self.x_pos > 0) or (log.speed > 0 and self.x_pos < log.surface.width - self.size):
            relative_seg_pos: list[int] = [
                abs((int(log.x_pos) + i * self.size) - int(self.x_pos)) for i in range(log.segments)
            ]
            closest_seg: int = min(relative_seg_pos)
            self.x_pos = log.x_pos + relative_seg_pos.index(closest_seg) * self.size

    def check_player_collision(self, player: Player) -> bool:
        return self.get_rect().colliderect(player.get_rect())
