import pygame
from game.constants import (
    GROUND_HEIGHT_MULTIPLIER,
    GROUND_START_MULTIPLIER,
    WATER_GRID_SPACING_MULTIPLIER,
    WATER_STARTING_ROW_ID,
)


class GenericObject:
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant


class EnvironmentObject(GenericObject):
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        super().__init__(surface, grid_constant)

        self.x_pos: float = 0
        self.y_pos: float = 0
        self.width: int = 0
        self.height: int = 0

        self.color: pygame.typing.ColorLike = "black"

    def get_rect(self):
        return pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.get_rect())


class EnvironmentManager(GenericObject):
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        super().__init__(surface, grid_constant)

        self.ground: Ground = Ground(surface=self.surface, grid_constant=self.grid_constant)
        self.water: WaterSystem = WaterSystem(surface=self.surface, grid_constant=self.grid_constant)

    def check_collisions(self, object: pygame.Rect) -> tuple[bool, float, float]:
        collided, aligned_x, aligned_y = self.ground.check_collisions(object=object)
        return collided, aligned_x, aligned_y

    def update(self, camera_offset):
        # self.water.update_grid(camera_offset=camera_offset)
        self.ground.update(camera_offset=camera_offset)

    def draw(self):
        # self.water.draw_grid()
        self.ground.draw()


class Ground(EnvironmentObject):
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        super().__init__(surface, grid_constant)

        self.width = self.surface.width
        self.height = self.grid_constant * GROUND_HEIGHT_MULTIPLIER
        self.x_pos = 0
        self.y_pos = self.surface.height - self.height + (GROUND_START_MULTIPLIER * self.grid_constant)

        self.color = "darkgreen"
        self.x_segments: int = self.width // self.grid_constant
        self.y_segments: int = self.height // self.grid_constant

    def update(self, camera_offset: float) -> None:
        self.y_pos += camera_offset

    def check_collisions(self, object: pygame.Rect) -> tuple[bool, float, float]:
        if self.get_rect().colliderect(object):
            aligned_x: float = self.get_aligned_x(object_x_pos=int(object.x))
            aligned_y: float = self.get_aligned_y(object_y_pos=int(object.y))
            return True, aligned_x, aligned_y
        return False, 0, 0

    def get_aligned_x(self, object_x_pos: int) -> int:
        closest_x: int = self.grid_constant
        closest_seg: int = 0
        for i in range(self.x_segments):
            relative_x = abs((int(self.x_pos) + i * self.grid_constant) - object_x_pos)
            if relative_x < closest_x:
                closest_x = relative_x
                closest_seg = i

        return int(self.x_pos + closest_seg * self.grid_constant)

    def get_aligned_y(self, object_y_pos: int) -> int:
        closest_y: int = self.grid_constant * self.y_segments
        closest_seg: int = 0
        for i in range(self.y_segments):
            relative_y = abs((int(self.y_pos) + i * self.grid_constant) - object_y_pos)
            if relative_y < closest_y:
                closest_y = relative_y
                closest_seg = i

        return int(self.y_pos + closest_seg * self.grid_constant)


class WaterSystem(GenericObject):
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        super().__init__(surface, grid_constant)

        self.top_row: int = (self.surface.height // self.grid_constant) + WATER_GRID_SPACING_MULTIPLIER

        self.water_grid: list[WaterRect] = [
            self.init_water_row(row_id=i * WATER_GRID_SPACING_MULTIPLIER + WATER_STARTING_ROW_ID)
            for i in range(self.top_row // WATER_GRID_SPACING_MULTIPLIER)
        ]

    def init_water_row(self, row_id: int) -> WaterRect:
        row: WaterRect = WaterRect(
            surface=self.surface,
            grid_constant=self.grid_constant,
            y_pos=self.surface.height - row_id * self.grid_constant,
        )
        return row

    def update_grid(self, camera_offset: float) -> None:
        for row in self.water_grid:
            row.update(camera_offset=camera_offset)

        if self.water_grid[-1].y_pos <= -(WATER_GRID_SPACING_MULTIPLIER * self.grid_constant):
            self.water_grid.remove(self.water_grid[-1])

        if self.water_grid[-1].y_pos >= 0:
            self.water_grid.append(self.init_water_row(row_id=self.top_row))

    def draw_grid(self) -> None:
        for row in self.water_grid:
            if row.y_pos < self.surface.height:
                row.draw()


class WaterRect(EnvironmentObject):
    def __init__(self, surface: pygame.Surface, grid_constant: int, y_pos: float) -> None:
        super().__init__(surface, grid_constant)

        self.width = self.surface.width
        self.height = self.grid_constant
        self.x_pos = 0
        self.y_pos = y_pos

        self.color = "blue"

    def update(self, camera_offset: float) -> None:
        self.y_pos += camera_offset
