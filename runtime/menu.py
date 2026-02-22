import pygame
from runtime.image import Image
from runtime.constants import IMAGE_SCALAR


class MenuManager:
    def __init__(self, surface: pygame.Surface, init_state: str) -> None:
        self.surface: pygame.Surface = surface
        self.game_state: str = init_state

        self.image: Image = Image(scalar=IMAGE_SCALAR)

        self.main_buttons: list[Button] = [
            Button(surface=self.surface, image=self.image.play_button(), pos=(20, 100), action="play"),
            Button(
                surface=self.surface, image=self.image.quit_button(), pos=(20, 100 + 25 * IMAGE_SCALAR), action="quit"
            ),
        ]
        self.main_menu: Menu = Menu(surface=self.surface, buttons=self.main_buttons, active_state="mainmenu")

        self.menus: list[Menu] = [self.main_menu]

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        for menu in self.menus:
            if self.game_state == menu.active_state:
                menu.update(viewport=viewport, scale=scale)
                if menu.return_state:
                    self.game_state = menu.return_state
                    menu.return_state = None

    def draw(self):
        for menu in self.menus:
            if self.game_state == menu.active_state:
                self.main_menu.draw()


class Menu:
    def __init__(
        self,
        surface: pygame.Surface,
        buttons: list[Button],
        active_state: str,
        bg_image: pygame.Surface | None = None,
        bg_color: pygame.typing.ColorLike | None = None,
    ) -> None:
        self.surface: pygame.Surface = surface
        self.buttons: list[Button] = buttons
        self.active_state: str = active_state

        self.bg_image: pygame.Surface | None = bg_image
        self.bg_color: pygame.typing.ColorLike | None = bg_color

        self.return_state: str | None = None

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        for button in self.buttons:
            button.update(viewport=viewport, scale=scale)
            if button.pressed:
                self.return_state = button.action

    def draw(self):
        for button in self.buttons:
            button.draw()


class Button:
    def __init__(self, surface: pygame.Surface, image: pygame.Surface, pos: tuple[int, int], action: str) -> None:
        self.surface: pygame.Surface = surface
        self.image: pygame.Surface = image
        self.pos: tuple[int, int] = pos
        self.action: str = action

        self.pressed: bool = False

        self.base_image: pygame.Surface = self.image
        self.glow_image: pygame.Surface = self.create_hue(offset=40)
        self.shadow_image: pygame.Surface = self.create_hue(offset=-40)

    def create_hue(self, offset: int) -> pygame.Surface:
        hue: pygame.Surface = self.image.copy()
        if offset < 0:
            amount: int = abs(offset)
            hue.fill((amount, amount, amount), special_flags=pygame.BLEND_RGB_SUB)

        else:
            amount: int = offset
            hue.fill((amount, amount, amount), special_flags=pygame.BLEND_RGB_ADD)

        return hue

    def scale_mouse(self, viewport: pygame.Rect, scale: int) -> tuple[int, int] | None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not viewport.collidepoint((mouse_x, mouse_y)):
            return None

        scale_x: int = (mouse_x - viewport.x) // scale
        scale_y: int = (mouse_y - viewport.y) // scale

        return scale_x, scale_y

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        mouse_pos: tuple[int, int] | None = self.scale_mouse(viewport=viewport, scale=scale)
        if not mouse_pos:
            return None

        touching: bool = self.image.get_rect(topleft=self.pos).collidepoint(mouse_pos)
        mouse_down: bool = pygame.mouse.get_pressed()[0]
        mouse_up: bool = pygame.mouse.get_just_released()[0]

        if touching:
            self.image = self.glow_image

            if mouse_down:
                self.image = self.shadow_image

            elif mouse_up:
                self.pressed = True

        else:
            self.image = self.base_image
            self.pressed = False

    def draw(self):
        self.surface.blit(self.image, self.pos)
