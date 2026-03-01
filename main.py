import pygame
from runtime.constants import SIZE_CONSTANT, SCREEN_CONSTANT, GameState as gs
from runtime.screen import Screen
from runtime.menu import MenuManager
from game.world import World

from runtime.music import Sfx


def get_delta_time(clock: pygame.Clock, fps: int) -> float:
    delta_time: float = clock.tick(fps) / 1000
    delta_time = min(0.1, max(0.001, delta_time))
    return delta_time


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Leap Frog")

    game_state: gs = gs.MAIN_MENU

    sfx: Sfx = Sfx()

    screen: Screen = Screen(screen_constant=SCREEN_CONSTANT, grid_constant=SIZE_CONSTANT)
    menu: MenuManager = MenuManager(surface=screen.alpha, init_state=game_state, sfx=sfx)
    world: World = World(surface=screen.logical, grid_constant=SIZE_CONSTANT, sfx=sfx)

    # -------------------------- Main Loop ------------------------
    while screen.running:

        delta_time: float = get_delta_time(clock=screen.clock, fps=screen.fps)
        if menu.game_state != game_state:
            if game_state == gs.MAIN_MENU and menu.game_state == gs.PLAY:
                world.restart()

            game_state = menu.game_state

        for event in pygame.event.get():
            if screen.running:
                screen.handle_events(event=event, game_state=game_state)

        if game_state == gs.PLAY:
            world.update_world(delta_time=delta_time)
        world.draw_world()

        menu.update(viewport=screen.viewport, scale=screen.scalar)
        menu.draw()

        screen.draw_overlay()
        screen.scale_flip()

    pygame.quit()
