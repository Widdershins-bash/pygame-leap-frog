import pygame
from random import randint

MAX_SPEED_MULTIPLIER: int = 5
STARTING_ROW_ID: int = 4


# TODO fix logRow genration and log.py organization
class GenericLog:
    def __init__(self, surface: pygame.Surface, girth: int) -> None:
        self.surface: pygame.Surface = surface
        self.girth: int = girth


class LogSystem(GenericLog):

    def __init__(self, surface: pygame.Surface, girth: int) -> None:
        super().__init__(surface, girth)

        self.height: int = self.surface.height
        self.min_speed: int = -(self.girth * MAX_SPEED_MULTIPLIER)
        self.max_speed: int = self.girth * MAX_SPEED_MULTIPLIER
        self.min_logs: int = 2
        self.max_logs: int = self.height // (self.girth * 2) - 2
        self.top_row: int = (self.height // self.girth) + 1
        self.rows: list[LogRow] = [
            self.init_row(row_id=i + STARTING_ROW_ID) for i in range(self.top_row - STARTING_ROW_ID)
        ]

    def init_row(self, row_id: int) -> LogRow:
        row: LogRow = LogRow(
            surface=self.surface,
            girth=self.girth,
            speed=randint(self.min_speed, self.max_speed),
            log_count=randint(self.min_logs, self.max_logs),
            row_id=row_id,
        )
        return row

    def update(self, camera_offset: float, delta_time: float) -> None:
        for row in self.rows:
            row.y_pos += camera_offset
            row.update(delta_time=delta_time)

        if self.rows[-1].y_pos <= -self.girth:
            self.rows.remove(self.rows[-1])

        if self.rows[-1].y_pos >= 0:
            self.rows.append(self.init_row(row_id=self.top_row))

    def check_collisions(self, object: pygame.Rect) -> tuple[bool, float, float]:
        for row in self.rows:
            collided, aligned_x, aligned_y = row.check_collisions(object)
            if collided:
                return collided, aligned_x, aligned_y
        return False, 0, 0

    def draw(self) -> None:
        for row in self.rows:
            if row.y_pos < self.surface.height:
                row.draw()


class LogRow(GenericLog):

    def __init__(self, surface: pygame.Surface, girth: int, speed: int, log_count: int, row_id: int) -> None:
        super().__init__(surface, girth)

        self.speed: int = speed or 20
        self.log_count: int = log_count
        self.row_id: int = row_id

        self.y_pos: float = self.surface.height - self.row_id * self.girth
        self.max_screen_segments: int = self.surface.width // self.girth
        self.max_log_segments: int = self.max_screen_segments // self.log_count - 1
        self.logs: list[Log] = [self.init_log(i) for i in range(self.log_count + 1)]

    def init_log(self, log_id: int) -> Log:
        log: Log = Log(
            surface=self.surface,
            girth=self.girth,
            speed=self.speed,
            segments=self.max_log_segments - randint(1, 2) if self.max_log_segments > 2 else self.max_log_segments,
            x_pos=log_id * (self.max_log_segments * self.girth + self.girth),
            y_pos=self.y_pos,
        )
        return log

    def update(self, delta_time: float) -> None:
        for log in self.logs:
            log.x_pos += self.speed * delta_time
            log.y_pos = self.y_pos
            log.check_respawn()

    def check_collisions(self, object: pygame.Rect) -> tuple[bool, float, float]:
        for log in self.logs:
            collided, aligned_x, aligned_y = log.check_collisions(object=object)
            if collided:
                return collided, aligned_x, aligned_y
        return False, 0, 0

    def draw(self) -> None:
        for log in self.logs:
            log.draw()


class Log(GenericLog):

    def __init__(
        self, surface: pygame.Surface, girth: int, speed: int, segments: int, x_pos: float, y_pos: float
    ) -> None:
        super().__init__(surface, girth)

        self.speed: int = speed
        self.segments: int = segments
        self.x_pos: float = x_pos
        self.y_pos: float = y_pos

    def get_aligned_x(self, object_x_pos: int) -> int:
        closest_x: int = self.girth
        closest_seg: int = 0
        for i in range(self.segments):
            relative_x = abs((int(self.x_pos) + i * self.girth) - object_x_pos)
            if relative_x < closest_x:
                closest_x = relative_x
                closest_seg = i

        return int(self.x_pos + closest_seg * self.girth)

    def check_respawn(self) -> None:
        if self.speed > 0 and self.x_pos > self.surface.width + self.girth:
            self.x_pos = 0 - self.segments * self.girth
        elif self.speed < 0 and self.x_pos < -self.girth - self.segments * self.girth:
            self.x_pos = self.surface.width

    def check_collisions(self, object: pygame.Rect) -> tuple[bool, float, float]:
        if self.get_rect().colliderect(object):
            aligned_x: float = self.get_aligned_x(object_x_pos=object.x)
            aligned_y: float = self.y_pos
            return True, aligned_x, aligned_y
        return False, 0, 0

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos, self.y_pos, self.girth * self.segments, self.girth)

    def draw(self) -> None:
        pygame.draw.rect(self.surface, "brown", self.get_rect())
