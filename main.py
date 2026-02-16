# Jam Theme: Flow
# TODO Make the game scroll when the player jumps forward
# -- Clean up LogManager
# -- Implement Camera system in main or Class
# TODO Add score counter
# TODO create controls GUI in blackspace
# TODO Leave it as death when reaching side of screen or implement a little scroll to increase the playfield


import pygame
from game.image import Image
from game.player import Player
from game.log import LogSystem


def get_delta_time(clock: pygame.Clock, fps: int) -> float:
    delta_time: float = clock.tick(fps) / 1000
    delta_time = min(0.1, max(0.001, delta_time))
    return delta_time


def display_fps(surface: pygame.Surface, clock: pygame.Clock, font: pygame.Font):
    fps_display: pygame.Surface = font.render(f"fps: {clock.get_fps():.0f}", True, "green", "black")
    surface.blit(fps_display)


if __name__ == "__main__":
    pygame.init()

    display_info = pygame.display.Info()
    PLAYER_SIZE: int = 30
    LOGICAL_SIZE: int = 480
    MARGIN: int = 100
    INITIAL_SCALE: int = min(display_info.current_w - MARGIN, display_info.current_h - MARGIN) // LOGICAL_SIZE
    WIDTH: int = LOGICAL_SIZE
    HEIGHT: int = LOGICAL_SIZE

    pygame.display.set_caption("HOP")

    fullscreen: bool = False
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    logical: pygame.Surface = pygame.Surface((LOGICAL_SIZE, LOGICAL_SIZE))

    fps_font: pygame.Font = pygame.Font("freesansbold.ttf", 10)
    text_font: pygame.Font = pygame.Font("freesansbold.ttf", 20)

    fps: int = 120
    clock: pygame.Clock = pygame.time.Clock()
    images: Image = Image()
    player: Player = Player(surface=logical, size=PLAYER_SIZE)
    log_system: LogSystem = LogSystem(surface=logical, girth=PLAYER_SIZE)

    grid: list[pygame.Rect] = [
        pygame.Rect(0, i * 2 * PLAYER_SIZE, LOGICAL_SIZE, PLAYER_SIZE)
        for i in range((LOGICAL_SIZE // PLAYER_SIZE) // 2)
    ]

    # -------------------------- Main Loop ------------------------

    running: bool = True
    while running:

        delta_time: float = get_delta_time(clock=clock, fps=fps)
        # ---------------------- Rendering -----------------------
        logical.fill("sky blue")
        for line in grid:
            pygame.draw.rect(logical, "blue", line)

        log_system.update(delta_time=delta_time)
        log_system.draw()
        player.update()
        player.draw()

        display_fps(surface=logical, clock=clock, font=fps_font)

        if not fullscreen:
            note_render: pygame.Surface = text_font.render("Press F for Fullscreen", False, "black")
            logical.blit(
                note_render,
                ((LOGICAL_SIZE - note_render.width) // 2, PLAYER_SIZE + (PLAYER_SIZE - note_render.height) // 2),
            )

        # ------------------------- End --------------------------

        for event in pygame.event.get():
            running = event.type != pygame.QUIT

            if event.type == pygame.KEYDOWN:
                running = event.key != pygame.K_ESCAPE or fullscreen

                if event.key == pygame.K_f:
                    if fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    fullscreen = not fullscreen

        scalar: int = max(1, min(screen.width // LOGICAL_SIZE, screen.height // LOGICAL_SIZE))
        display: pygame.Surface = pygame.transform.scale(logical, (LOGICAL_SIZE * scalar, LOGICAL_SIZE * scalar))
        screen.blit(display, ((screen.width - display.width) // 2, (screen.height - display.height) // 2))
        pygame.display.flip()

    pygame.quit()
