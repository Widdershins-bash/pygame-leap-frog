# Jam Theme: Flow

# River tycoon: how big and clean can you make your river?
# To keep it simple, I need to make the upgrade system simple and the obstacles simple.
#

import pygame
from game.image import Image
from game.player import Player


def get_delta_time(clock: pygame.Clock, fps: int) -> float:
    delta_time: float = clock.tick(fps) / 1000
    delta_time = min(0.1, max(0.001, delta_time))
    return delta_time


if __name__ == "__main__":
    pygame.init()

    display_info = pygame.display.Info()
    LOGICAL_SIZE: int = 320
    MARGIN: int = 100
    INITIAL_SCALE: int = min(display_info.current_w - 100, display_info.current_h - 100) // LOGICAL_SIZE
    WIDTH: int = LOGICAL_SIZE * INITIAL_SCALE
    HEIGHT: int = LOGICAL_SIZE * INITIAL_SCALE

    pygame.display.set_caption("CAPTION")

    fullscreen: bool = False
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    logical: pygame.Surface = pygame.Surface((LOGICAL_SIZE, LOGICAL_SIZE))

    fps: int = 60
    clock: pygame.Clock = pygame.time.Clock()
    images: Image = Image()
    player: Player = Player(logical)

    # ------------------------ Main Loop ------------------------
    running: bool = True
    while running:

        delta_time: float = get_delta_time(clock=clock, fps=fps)

        logical.fill("sky blue")

        player.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_f:
                    if fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    fullscreen = not fullscreen

        scalar: int = max(1, min(screen.width // LOGICAL_SIZE, screen.height // LOGICAL_SIZE))
        display: pygame.Surface = pygame.transform.scale(logical, (logical.width * scalar, logical.height * scalar))
        screen.blit(display, ((screen.width - display.width) // 2, (screen.height - display.height) // 2))
        pygame.display.flip()

    pygame.quit()
