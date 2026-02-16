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

    def check_collision(self, rect_a: pygame.Rect, rect_b: pygame.Rect) -> bool:
        return rect_a.colliderect(rect_b)

    def check_player_log_collision(self) -> None:
        for row in self.logs.rows:
            for log in row.logs:
                if self.check_collision(self.player.get_rect(), log.get_rect()):
                    aligned_x = log.get_aligned_pos(object_x_pos=int(self.player.x_pos))
                    self.player.land_on_log(aligned_x_pos=aligned_x)

    def update_collisions(self) -> None:
        self.check_player_log_collision()
        self.player.check_boundary_collision()

    def update_world(self, delta_time: float) -> None:
        self.logs.update(delta_time=delta_time)
        self.player.update()

        self.update_collisions()

    def draw_world(self) -> None:
        self.surface.fill("sky blue")
        self.draw_grid()
        self.logs.draw()
        self.player.draw()
