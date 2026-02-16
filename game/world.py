import pygame
from game.player import Player
from game.log import LogSystem
from game.camera import Camera


class World:
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.player: Player = Player(surface=self.surface, size=self.grid_constant)
        self.logs: LogSystem = LogSystem(surface=self.surface, girth=self.grid_constant)
        self.camera: Camera = Camera()

        self.water_grid: list[pygame.Rect] = [
            pygame.Rect(0, i * 2 * self.grid_constant, self.surface.height, self.grid_constant)
            for i in range((self.surface.height // self.grid_constant) // 2)
        ]

    def draw_grid(self) -> None:
        for line in self.water_grid:
            pygame.draw.rect(self.surface, "blue", line)

    def draw_world(self) -> None:
        self.surface.fill("sky blue")
        self.draw_grid()
        self.logs.draw()
        self.player.draw()

    def update_world(self, delta_time: float) -> None:
        self.logs.update(delta_time=delta_time)
        self.player.update()

    # def set_onlog(self, log: Log) -> None:
    #     if (log.speed < 0 and self.x_pos > 0) or (log.speed > 0 and self.x_pos < log.surface.width - self.size):
    #         relative_seg_pos: list[int] = [
    #             abs((int(log.x_pos) + i * self.size) - int(self.x_pos)) for i in range(log.segments)
    #         ]
    #         closest_seg: int = min(relative_seg_pos)
    #         self.x_pos = log.x_pos + relative_seg_pos.index(closest_seg) * self.size

    # def check_player_collision(self, player: Player) -> bool:
    #     return self.get_rect().colliderect(player.get_rect())
