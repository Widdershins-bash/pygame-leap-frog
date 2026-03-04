import pygame
from game.player import Player
from game.log import LogSystem
from game.environment import EnvironmentManager
from game.camera import Camera
from runtime.constants import SCORE_OFFSET, ColorPalette as cp
from runtime.music import Sfx


class World:

    def __init__(self, surface: pygame.Surface, grid_constant: int, sfx: Sfx) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant
        self.sfx: Sfx = sfx

        self.player: Player = Player(surface=self.surface, size=self.grid_constant)
        self.logs: LogSystem = LogSystem(surface=self.surface, girth=self.grid_constant)
        self.environment: EnvironmentManager = EnvironmentManager(
            surface=self.surface, grid_constant=self.grid_constant
        )
        self.camera: Camera = Camera(player_y=self.player.y_pos, grid_constant=self.grid_constant)

        self.camera_offset: float = self.camera.y_offset

        self.font: pygame.Font = pygame.Font("freesansbold.ttf")
        self.score_display: pygame.Surface | None = None
        self.last_score: int = -1

    def update_score(self) -> None:
        score: int = max(self.player.score + SCORE_OFFSET, 0)
        if score != self.last_score:
            self.score_display = self.font.render(f"{score}", True, cp.DEFAULT)
            self.last_score = score

    def draw_score(self) -> None:
        if self.score_display:
            self.surface.blit(self.score_display, (0, 40))

    def check_collision(self, rect_a: pygame.Rect, rect_b: pygame.Rect) -> bool:
        return rect_a.colliderect(rect_b)

    def check_player_log_collision(self) -> None:
        collided, aligned_x, aligned_y = self.logs.check_collisions(object=self.player.get_rect())
        if collided:
            self.player.land_on_object(aligned_x_pos=aligned_x, aligned_y_pos=aligned_y)

    def check_player_environment_collision(self) -> None:
        collided, aligned_x, aligned_y = self.environment.check_collisions(object=self.player.get_rect())
        if collided:
            self.player.land_on_object(aligned_x_pos=aligned_x, aligned_y_pos=aligned_y)

    def update_collisions(self) -> None:
        self.check_player_log_collision()
        self.check_player_environment_collision()
        self.player.check_boundary_collision()

    def update_world(self, delta_time: float) -> None:
        self.environment.update(camera_offset=self.camera_offset)
        self.logs.update(camera_offset=self.camera_offset, delta_time=delta_time)
        self.player.update(
            camera_offset=self.camera_offset,
            respawn_pos=self.environment.ground.y_pos + self.environment.ground.height // 2 - self.grid_constant,
        )

        self.update_collisions()
        self.update_score()
        self.camera_offset = self.camera.get_offset(new_player_y=self.player.y_pos, delta_time=delta_time)

    def draw_world(self) -> None:
        self.surface.fill(cp.WATER)
        self.environment.draw()
        self.logs.draw()
        self.player.draw()
        self.draw_score()

    def restart(self):
        self.__init__(surface=self.surface, grid_constant=self.grid_constant, sfx=self.sfx)
