import pygame

LOGICAL_SIZE: int = 480
MARGIN: int = 100
FPS: int = 120


class Screen:
    def __init__(self, grid_constant: int) -> None:
        self.grid_constant: int = grid_constant

        self.logical_size: int = LOGICAL_SIZE
        self.margin: int = MARGIN
        self.font: pygame.Font = pygame.Font("freesansbold.ttf", 11)

        self.fps: int = FPS
        self.clock: pygame.Clock = pygame.time.Clock()

        self.running: bool = True
        self.fullscreen: bool = False

        self.screen: pygame.Surface = pygame.display.set_mode((self.logical_size, self.logical_size), pygame.RESIZABLE)
        self.logical: pygame.Surface = pygame.Surface((self.logical_size, self.logical_size))

    def display_fps(self):
        fps_display: pygame.Surface = self.font.render(f"fps: {self.clock.get_fps():.0f}", True, "green", "black")
        self.logical.blit(fps_display)

    def display_tips(self):
        if not self.fullscreen:
            note_render: pygame.Surface = self.font.render("Press F for Fullscreen", False, "black")
            self.logical.blit(
                note_render,
                (
                    (self.logical_size - note_render.width) // 2,
                    self.grid_constant + (self.grid_constant - note_render.height) // 2,
                ),
            )

    def handle_events(self, event: pygame.Event) -> None:
        self.running = event.type != pygame.QUIT

        if event.type == pygame.KEYDOWN:
            self.running = event.key != pygame.K_ESCAPE or self.fullscreen

            if event.key == pygame.K_f:
                if self.fullscreen:
                    self.screen = pygame.display.set_mode((self.logical_size, self.logical_size), pygame.RESIZABLE)

                else:
                    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.fullscreen = not self.fullscreen

    def draw_overlay(self) -> None:
        self.display_fps()
        self.display_tips()

    def scale_flip(self) -> None:

        scalar: int = max(1, min(self.screen.width, self.screen.height) // self.logical_size)
        logical_transform: pygame.Surface = pygame.transform.scale(
            self.logical, (self.logical_size * scalar, self.logical_size * scalar)
        )
        self.screen.blit(
            logical_transform,
            ((self.screen.width - logical_transform.width) // 2, (self.screen.height - logical_transform.height) // 2),
        )
        pygame.display.flip()
