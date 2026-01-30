# Jam Theme: Flow

# Ideas:
# 1. Crossy road with water and logs only
# 2. River tycoon: how big and clean can you make your river?


import pygame
from logic.image import Image


def get_delta_time(clock: pygame.Clock, fps: int) -> float:
    delta_time: float = clock.tick(fps) / 1000
    delta_time = min(0.1, max(0.001, delta_time))
    return delta_time


if __name__ == "__main__":
    pygame.init()

    WIDTH: int = 800
    HEIGHT: int = 800

    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))

    fps: int = 60
    clock: pygame.Clock = pygame.time.Clock()
    images: Image = Image()

    x: float = 0
    # ------------------------ Main Loop ------------------------
    running: bool = True
    while running:

        delta_time: float = get_delta_time(clock=clock, fps=fps)
        screen.fill("white")

        screen.blit(images.boat_img, (x, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
