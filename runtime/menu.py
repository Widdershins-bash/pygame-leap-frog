import pygame
from runtime.button import ButtonConfig, Button, VolumeSlider
from runtime.constants import MENU_MARGIN, ColorPalette as cp, GameState as gs
from runtime.music import Sfx


class MenuManager:
    def __init__(self, surface: pygame.Surface, init_state: gs, sfx: Sfx) -> None:
        self.surface: pygame.Surface = surface
        self.game_state: gs = init_state
        self.memory_state: gs | None = None

        self.sfx: Sfx = sfx

        self.button: ButtonConfig = ButtonConfig(surface=self.surface)

        self.main_menu: Menu = Menu(
            surface=self.surface, buttons=self.button.main_buttons, active_state=gs.MAIN_MENU, bg_color=cp.SAND
        )
        self.settings_widget: Menu = Menu(
            surface=self.surface, buttons=[self.button.settings_widget], is_widget=True, active_state=gs.MAIN_MENU
        )
        self.settings_menu: Menu = Menu(
            surface=self.surface, buttons=self.button.settings_buttons, active_state=gs.SETTINGS, bg_color=cp.SAND
        )
        self.pause_widget: Menu = Menu(
            surface=self.surface, buttons=[self.button.pause_widget], is_widget=True, active_state=gs.PLAY
        )
        self.pause_menu: Menu = Menu(
            surface=self.surface, buttons=self.button.pause_buttons, active_state=gs.PAUSE, bg_color=cp.ALPHA_SAND
        )

        self.menus: list[Menu] = [
            self.pause_widget,
            self.pause_menu,
            self.main_menu,
            self.settings_widget,
            self.settings_menu,
        ]

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        for menu in self.menus:
            if self.game_state == menu.active_state or menu.always_visible:
                menu.update(viewport=viewport, scale=scale, sfx=self.sfx)
                if menu.opened and not menu.is_widget:
                    self.sfx.swoosh_sfx.play()

                if menu.return_state:
                    self.game_state = menu.return_state
                    break
            else:
                menu.deactivate()

    def draw(self) -> None:
        for menu in self.menus:
            if self.game_state == menu.active_state or menu.always_visible:
                menu.draw()


class Menu:
    def __init__(
        self,
        surface: pygame.Surface,
        buttons: list[Button],
        active_state: gs | None = None,
        is_widget: bool | None = None,
        always_visible: bool = False,
        bg_image: pygame.Surface | None = None,
        bg_color: pygame.typing.ColorLike | None = None,
    ) -> None:
        self.surface: pygame.Surface = surface
        self.buttons: list[Button] = buttons
        self.always_visible: bool = always_visible
        self.active_state: gs | None = active_state
        self.is_widget: bool | None = is_widget

        self.ping_open: bool = False
        self.opened: bool = False

        if not self.is_widget:
            self.set_positions()

        self.bg_image: pygame.Surface | None = bg_image
        self.bg_color: pygame.typing.ColorLike | None = bg_color
        self.bg_rect: pygame.Rect = pygame.Rect(0, 0, self.surface.width, self.surface.height)

        self.return_state: gs | None = None

    def set_positions(self) -> None:
        spacing: int = MENU_MARGIN
        n: int = len(self.buttons)

        for i, button in enumerate(self.buttons):
            index_height: int = spacing + button.display_image.height

            x: int = (self.surface.width - button.display_image.width) // 2
            y: int = (self.surface.height - (n * index_height)) // 2 + (i * index_height)

            button.pos = (x, y)

    def check_open(self) -> None:
        self.opened = False

        if not self.ping_open:
            self.opened = True
            self.ping_open = True

    def deactivate(self) -> None:
        self.ping_open = False
        self.opened = False
        self.return_state = None
        for button in self.buttons:
            button.prep_state()

    def update(self, viewport: pygame.Rect, scale: int, sfx: Sfx) -> None:
        self.check_open()
        for button in self.buttons:
            button.update(viewport=viewport, scale=scale)

            if button.clicked:
                sfx.click_sfx.play()
                self.return_state = button.action

            if button.focused:
                sfx.hover_sfx.play()

            if isinstance(button, VolumeSlider):
                if button.set_volume:
                    sfx.audio_state.set_volume(value=button.volume)
                    sfx.update_volume()
                else:
                    button.sync_volume(sfx.audio_state.volume)

    def draw(self) -> None:
        if self.bg_color:
            pygame.draw.rect(self.surface, self.bg_color, self.bg_rect)

        for button in self.buttons:
            button.draw()
