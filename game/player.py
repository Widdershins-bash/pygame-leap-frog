import pygame
from game.constants import RECT_SIZE_DECREASE, MARGIN_DECREASE


class Player:

    def __init__(self, surface: pygame.Surface, size: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = size

        self.rect_size: float = self.size - self.size * RECT_SIZE_DECREASE
        self.margin: float = self.size - self.size * MARGIN_DECREASE

        self.in_water: bool = True

        self.x_pos, self.y_pos = self.start_pos()
        self.speed_offset: int = 0
        # Refactor score in the future to be entirely handled by world (if new point methods are added)
        self.score: int = 0

    def start_pos(self) -> tuple[float, float]:
        x: float = (self.surface.width - self.size) // 2
        y: float = self.surface.height - self.size
        return (x, y)

    def respawn(self, pos: float):
        self.y_pos = pos
        self.x_pos = self.start_pos()[0]
        self.score = 0

    def check_boundary_collision(self) -> None:
        if self.x_pos < 0:
            self.x_pos = 0
        if self.x_pos > self.surface.width - self.size:
            self.x_pos = self.surface.width - self.size

    def land_on_object(self, aligned_x_pos: float, aligned_y_pos: float) -> None:
        self.x_pos = aligned_x_pos
        self.y_pos = aligned_y_pos
        self.in_water = False

    def handle_movement(self) -> None:
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            self.y_pos -= self.size
            self.score += 1

        if pygame.key.get_just_pressed()[pygame.K_RIGHT]:
            self.x_pos += self.size

        if pygame.key.get_just_pressed()[pygame.K_LEFT]:
            self.x_pos -= self.size

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos + self.margin, self.y_pos + self.margin, self.rect_size, self.rect_size)

    def draw(self) -> None:
        pygame.draw.rect(self.surface, "green", self.get_rect(), border_radius=self.size // 2)

    def update(self, camera_offset: float, respawn_pos: float) -> None:
        self.y_pos += camera_offset
        self.handle_movement()
        if self.in_water:
            self.respawn(pos=respawn_pos)

        self.in_water = True
