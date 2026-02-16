import pygame
from game.world import World
from runtime.screen import Screen


def get_delta_time(clock: pygame.Clock, fps: int) -> float:
    delta_time: float = clock.tick(fps) / 1000
    delta_time = min(0.1, max(0.001, delta_time))
    return delta_time


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Leap Frog")

    SIZE_CONSTANT: int = 30

    screen: Screen = Screen(grid_constant=SIZE_CONSTANT)
    world: World = World(surface=screen.logical, grid_constant=SIZE_CONSTANT)

    # -------------------------- Main Loop ------------------------

    while screen.running:

        delta_time: float = get_delta_time(clock=screen.clock, fps=screen.fps)

        for event in pygame.event.get():
            screen.handle_events(event=event)

        world.update_world(delta_time=delta_time)
        world.draw_world()

        screen.draw_overlay()
        screen.scale_flip()

    pygame.quit()
