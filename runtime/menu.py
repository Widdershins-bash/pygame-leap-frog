import pygame
from runtime.button import ButtonConfig, Button
from runtime.constants import BUTTON_SCALAR, ColorPalette as cp, GameState as gs


# TODO figure out how I want to display the buttons and the background I want for them
# - I want a legit background for the main menu, but then I will create an alpha surface for the options menu
# - I want the legit background to be water with a few logs floating across it
# - I want everything to be centered.
class MenuManager:
    def __init__(self, surface: pygame.Surface, init_state: str) -> None:
        self.surface: pygame.Surface = surface
        self.game_state: str = init_state

        self.button: ButtonConfig = ButtonConfig(surface=self.surface)

        self.main_menu: Menu = Menu(
            surface=self.surface, buttons=self.button.main_buttons, active_state=gs.MAIN_MENU, bg_color=cp.SAND
        )
        self.settings_widget: Menu = Menu(
            surface=self.surface, buttons=[self.button.settings_widget], active_state=gs.ACTIVE, auto_pos=False
        )
        self.settings_menu: Menu = Menu(
            surface=self.surface, buttons=self.button.settings_buttons, active_state=gs.SETTINGS
        )

        self.menus: list[Menu] = [self.main_menu, self.settings_widget, self.settings_menu]

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        for menu in self.menus:
            if self.game_state == menu.active_state or menu.active_state == gs.ACTIVE:
                menu.update(viewport=viewport, scale=scale)
                if menu.return_state:
                    self.game_state = menu.return_state
                    menu.return_state = None

    def draw(self) -> None:
        for menu in self.menus:
            if self.game_state == menu.active_state or menu.active_state == gs.ACTIVE:
                menu.draw()


class Menu:
    def __init__(
        self,
        surface: pygame.Surface,
        buttons: list[Button],
        active_state: str,
        auto_pos: bool = True,
        bg_image: pygame.Surface | None = None,
        bg_color: pygame.typing.ColorLike | None = None,
    ) -> None:
        self.surface: pygame.Surface = surface
        self.buttons: list[Button] = buttons
        self.auto_pos: bool = auto_pos
        self.active_state: str = active_state

        if self.auto_pos:
            self.set_positions()

        self.bg_image: pygame.Surface | None = bg_image
        self.bg_color: pygame.typing.ColorLike | None = bg_color
        self.bg_rect: pygame.Rect = pygame.Rect(0, 0, self.surface.width, self.surface.height)

        self.return_state: str | None = None

    def set_positions(self):
        spacing: int = BUTTON_SCALAR * 2
        n: int = len(self.buttons)

        for i, button in enumerate(self.buttons):
            index_height: int = spacing + button.image.height

            x: int = (self.surface.width - button.image.width) // 2
            y: int = (self.surface.height - (n * index_height)) // 2 + (i * index_height)

            button.pos = (x, y)

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        for button in self.buttons:
            button.update(viewport=viewport, scale=scale)
            if button.pressed:
                self.return_state = button.action

    def draw(self) -> None:
        if self.bg_color:
            pygame.draw.rect(self.surface, self.bg_color, self.bg_rect)

        for button in self.buttons:
            button.draw()
