import pygame


class Player:

    def __init__(self, surface: pygame.Surface, size: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = size

        self.speed_offset: int = 0
        self.margin: int = self.size // 10
        self.splashed: bool = True

        self.x_pos: float
        self.y_pos: float
        self.goto_start()

    def start_pos(self) -> tuple[float, float]:
        x: float = (self.surface.width - self.size) // 2
        y: float = self.surface.height - self.size
        return (x, y)

    def goto_start(self):
        self.x_pos, self.y_pos = self.start_pos()

    def move(self, x: int = 0, y: int = 0):
        self.x_pos += x
        self.y_pos += y

    def handle_movement(self):
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            self.move(y=-self.size)

        if pygame.key.get_just_pressed()[pygame.K_RIGHT]:
            self.move(x=self.size)

        if pygame.key.get_just_pressed()[pygame.K_LEFT]:
            self.move(x=-self.size)

        if self.y_pos == -self.size:
            self.goto_start()

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos + 3.5, self.y_pos + 3.5, self.size - 7, self.size - 7)

    def draw(self):
        pygame.draw.rect(self.surface, "green", self.get_rect(), border_radius=self.size // 2)

    def update(self):
        if self.splashed:
            self.goto_start()
        self.splashed = True

        self.handle_movement()
        self.draw()
