import pygame
from runtime.constants import SCREEN_MARGIN, FPS, ColorPalette as cp, GameState as gs


class Screen:
    def __init__(self, screen_constant: int, grid_constant: int) -> None:
        self.grid_constant: int = grid_constant

        self.logical_size: int = screen_constant
        self.margin: int = SCREEN_MARGIN
        self.fps_font: pygame.Font = pygame.Font("freesansbold.ttf", 12)
        self.tip_font: pygame.Font = pygame.Font("freesansbold.ttf")

        self.fps: int = FPS
        self.clock: pygame.Clock = pygame.time.Clock()

        self.running: bool = True
        self.fullscreen: bool = False

        self.screen: pygame.Surface = pygame.display.set_mode((self.logical_size, self.logical_size), pygame.RESIZABLE)
        self.logical: pygame.Surface = pygame.Surface((self.logical_size, self.logical_size))
        self.viewport: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.scalar: int = 1

    def display_fps(self) -> None:
        fps_display: pygame.Surface = self.fps_font.render(f"fps: {self.clock.get_fps():.0f}", True, cp.FPS, cp.DEFAULT)
        self.logical.blit(fps_display)

    def display_tips(self) -> None:
        if not self.fullscreen:
            note_message: str = "Press F for Fullscreen"
            note_render: pygame.Surface = self.tip_font.render(note_message, False, cp.DEFAULT)
            note_pos: tuple[int, int] = (
                (self.logical_size - note_render.width) // 2,
                self.grid_constant + (self.grid_constant - note_render.height) // 2,
            )
            self.logical.blit(note_render, note_pos)

    def handle_events(self, event: pygame.Event, game_state: str) -> None:
        self.running = event.type != pygame.QUIT
        if game_state == gs.QUIT:
            self.running = False

        if event.type == pygame.KEYDOWN:
            self.running = event.key != pygame.K_ESCAPE or self.fullscreen  # temporary escape for testing

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

        self.scalar = max(1, min(self.screen.width, self.screen.height) // self.logical_size)
        scale_point: tuple[int, int] = (self.logical_size * self.scalar, self.logical_size * self.scalar)
        logical_transform: pygame.Surface = pygame.transform.scale(self.logical, scale_point)
        logical_location: tuple[int, int] = (
            (self.screen.width - logical_transform.width) // 2,
            (self.screen.height - logical_transform.height) // 2,
        )

        self.viewport = pygame.Rect(logical_location, scale_point)
        self.screen.blit(logical_transform, logical_location)

        pygame.display.flip()
