import pygame

SIZE_DECREASE_CONSTANT: int = 5
RECT_SIZE_DECREASE: float = 1 / SIZE_DECREASE_CONSTANT
MARGIN_DECREASE: float = (SIZE_DECREASE_CONSTANT * 2 - 1) / (SIZE_DECREASE_CONSTANT * 2)


class Player:

    def __init__(self, surface: pygame.Surface, size: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = size
        self.rect_size: float = self.size - self.size * RECT_SIZE_DECREASE
        self.margin: float = self.size - self.size * MARGIN_DECREASE

        self.x_pos, self.y_pos = self.start_pos()
        self.speed_offset: int = 0

    def start_pos(self) -> tuple[float, float]:
        x: float = (self.surface.width - self.size) // 2
        y: float = self.surface.height - self.size
        return (x, y)

    def goto_start(self) -> None:
        self.x_pos, self.y_pos = self.start_pos()

    def handle_movement(self) -> None:
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            self.y_pos -= self.size

        if pygame.key.get_just_pressed()[pygame.K_RIGHT]:
            self.x_pos += self.size

        if pygame.key.get_just_pressed()[pygame.K_LEFT]:
            self.x_pos -= self.size

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos + self.margin, self.y_pos + self.margin, self.rect_size, self.rect_size)

    def draw(self):
        pygame.draw.rect(self.surface, "green", self.get_rect(), border_radius=self.size // 2)

    def update(self) -> None:
        self.handle_movement()
        if self.y_pos == -self.size:
            self.goto_start()
