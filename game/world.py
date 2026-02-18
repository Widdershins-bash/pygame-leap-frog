import pygame
from game.player import Player
from game.log import LogSystem
from game.enviroment import EnviromentManager
from game.camera import Camera


class World:

    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.player: Player = Player(surface=self.surface, size=self.grid_constant)
        self.logs: LogSystem = LogSystem(surface=self.surface, girth=self.grid_constant)
        self.enviroment: EnviromentManager = EnviromentManager(surface=self.surface, grid_constant=self.grid_constant)
        self.camera: Camera = Camera(player_y=self.player.y_pos, grid_constant=self.grid_constant)

        self.camera_offset: float = self.camera.y_offset
        self.font: pygame.Font = pygame.Font("freesansbold.ttf")

    def display_score(self):
        score: int = self.player.score - 2  # THRESHOLD_MULTIPLIER - 1
        score_display: pygame.Surface = self.font.render(f"{score if score > 0 else 0}", False, "black")
        self.surface.blit(score_display, (0, 40))

    def check_collision(self, rect_a: pygame.Rect, rect_b: pygame.Rect) -> bool:
        return rect_a.colliderect(rect_b)

    def check_player_log_collision(self) -> None:
        collided, aligned_x, aligned_y = self.logs.check_collisions(object=self.player.get_rect())
        if collided:
            self.player.land_on_object(aligned_x_pos=aligned_x, aligned_y_pos=aligned_y)

    def check_player_enviroment_collision(self) -> None:
        collided, aligned_x, aligned_y = self.enviroment.check_collisions(object=self.player.get_rect())
        if collided:
            self.player.land_on_object(aligned_x_pos=aligned_x, aligned_y_pos=aligned_y)

    def update_collisions(self) -> None:
        self.check_player_log_collision()
        self.check_player_enviroment_collision()
        self.player.check_boundary_collision()

    def update_world(self, delta_time: float) -> None:
        self.enviroment.update(camera_offset=self.camera_offset)
        self.logs.update(camera_offset=self.camera_offset, delta_time=delta_time)
        self.player.update(
            camera_offset=self.camera_offset,
            respawn_pos=self.enviroment.ground.y_pos + self.enviroment.ground.height // 2 - self.grid_constant,
        )
        self.update_collisions()

        self.camera_offset = self.camera.get_offset(new_player_y=self.player.y_pos, delta_time=delta_time)

    def draw_world(self) -> None:
        self.surface.fill("sky blue")
        self.enviroment.draw()
        self.logs.draw()
        self.player.draw()

        self.display_score()
