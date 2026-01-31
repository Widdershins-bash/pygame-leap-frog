# Jam Theme: Flow

# River tycoon: how big and clean can you make your river?
# To keep it simple, I need to make the upgrade system simple and the obstacles simple.
#

import pygame
from game.image import Image
from game.player import Player
from game.log import Log


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
    PLAYER_SIZE: int = 40
    LOGICAL_SIZE: int = 320
    MARGIN: int = 100
    INITIAL_SCALE: int = min(display_info.current_w - 100, display_info.current_h - 100) // LOGICAL_SIZE
    WIDTH: int = LOGICAL_SIZE * INITIAL_SCALE
    HEIGHT: int = LOGICAL_SIZE * INITIAL_SCALE

    pygame.display.set_caption("HOP")

    fullscreen: bool = False
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    logical: pygame.Surface = pygame.Surface((LOGICAL_SIZE, LOGICAL_SIZE))
    font: pygame.Font = pygame.font.Font("freesansbold.ttf", 10)

    fps: int = 120
    clock: pygame.Clock = pygame.time.Clock()
    images: Image = Image()
    player: Player = Player(surface=logical, size=PLAYER_SIZE)

    # ------------------------ Main Loop ------------------------

    logs: list[Log] = [Log(surface=logical, log_girth=PLAYER_SIZE) for _ in range(50)]
    travel_distance: int = 0
    stop_watch: float = 0
    running: bool = True
    while running:

        delta_time: float = get_delta_time(clock=clock, fps=fps)

        logical.fill("sky blue")

        for log in logs:
            if player.jumped:
                log.y_pos += PLAYER_SIZE
            log.x_pos -= max(0.001, log.speed * delta_time)
            log.draw()

            if log.x_pos < 0 - log.log_length or log.y_pos >= LOGICAL_SIZE:
                logs.remove(log)
                logs.append(Log(surface=logical, log_girth=PLAYER_SIZE))

        player.jumped = False

        player.draw(((LOGICAL_SIZE - PLAYER_SIZE) // 2, LOGICAL_SIZE - PLAYER_SIZE * 2))
        display_fps(surface=logical, clock=clock, font=font)

        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            player.jumped = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not fullscreen:
                    running = False

                if event.key == pygame.K_f:
                    if fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    fullscreen = not fullscreen

        stop_watch += 1 * delta_time
        scalar: int = max(1, min(screen.width // LOGICAL_SIZE, screen.height // LOGICAL_SIZE))
        display: pygame.Surface = pygame.transform.scale(logical, (LOGICAL_SIZE * scalar, LOGICAL_SIZE * scalar))
        screen.blit(display, ((screen.width - display.width) // 2, (screen.height - display.height) // 2))
        pygame.display.flip()

    pygame.quit()
