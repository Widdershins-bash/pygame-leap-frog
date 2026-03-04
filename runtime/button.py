import pygame
from runtime.image import ImageManager, ButtonSprite
from runtime.constants import BUTTON_SCALAR, MENU_MARGIN, GameState as gs


class ButtonConfig:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface: pygame.Surface = surface

        self.image: ImageManager = ImageManager(scalar=BUTTON_SCALAR)
        self.sprite: ButtonSprite = self.image.button

        self.main_buttons: list[Button] = [
            ActionButton(surface=self.surface, image=self.sprite.play, action=gs.PLAY),
            ActionButton(surface=self.surface, image=self.sprite.quit, action=gs.QUIT),
        ]

        self.settings_widget: Button = ActionButton(
            surface=self.surface,
            image=self.sprite.settings,
            action=gs.SETTINGS,
            pos=(self.surface.width - self.sprite.y_scalar - MENU_MARGIN, MENU_MARGIN),
        )

        self.settings_buttons: list[Button] = [
            ActionButton(surface=self.surface, image=self.sprite.menu, action=gs.MAIN_MENU),
            VolumeSlider(surface=self.surface, image=self.sprite.volume),
        ]

        self.pause_widget: Button = ActionButton(
            surface=self.surface,
            image=self.sprite.settings,
            action=gs.PAUSE,
            pos=(self.surface.width - self.sprite.y_scalar - MENU_MARGIN, MENU_MARGIN),
        )
        self.pause_buttons: list[Button] = [
            ActionButton(surface=self.surface, image=self.sprite.resume, action=gs.PLAY),
            ActionButton(surface=self.surface, image=self.sprite.menu, action=gs.MAIN_MENU),
            VolumeSlider(surface=self.surface, image=self.sprite.volume),
        ]


class Button:

    def __init__(
        self,
        surface: pygame.Surface,
        image: pygame.Surface,
        enabled: bool = True,
        action: gs | None = None,
        pos: tuple[int, int] = (0, 0),
    ) -> None:
        self.surface: pygame.Surface = surface
        self.display_image: pygame.Surface = image
        self.enabled: bool = enabled
        self.action: gs | None = action
        self.pos: tuple[int, int] = pos

        self.clicked: bool = False
        self.click_source: bool = False
        self.ping_focused: bool = False
        self.focused: bool = False
        self.touching: bool = False

        self.mouse_pos: tuple[int, int] | None = None

        self.base_image: pygame.Surface = self.display_image
        self.glow_image: pygame.Surface = self.create_hue(offset=40)
        self.shadow_image: pygame.Surface = self.create_hue(offset=-40)

    def create_hue(self, offset: int) -> pygame.Surface:
        hue: pygame.Surface = self.display_image.copy()
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

    def check_click(self) -> None:
        mouse_down: bool = pygame.mouse.get_pressed()[0]
        mouse_up: bool = pygame.mouse.get_just_released()[0]

        if mouse_down:
            self.display_image = self.shadow_image

        elif mouse_up:
            self.clicked = True

    def check_focus(self):
        self.display_image = self.glow_image

        self.focused = False

        if not self.ping_focused:
            self.focused = True
            self.ping_focused = True

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        self.mouse_pos = self.scale_mouse(viewport=viewport, scale=scale)
        if not self.mouse_pos:
            return

        if not self.enabled:
            self.display_image = self.shadow_image
            return

        self.touching = self.display_image.get_rect(topleft=self.pos).collidepoint(self.mouse_pos)

    def draw(self) -> None:
        self.surface.blit(self.display_image, self.pos)

    def clear_state(self) -> None:
        self.clicked = False
        self.click_source = False
        self.check_for_click = False
        self.ping_focused = False
        self.focused = False
        self.touching = False
        self.display_image = self.base_image


class ActionButton(Button):

    def __init__(
        self,
        surface: pygame.Surface,
        image: pygame.Surface,
        enabled: bool = True,
        action: gs | None = None,
        pos: tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__(surface, image, enabled, action, pos)

    def update(self, viewport: pygame.Rect, scale: int):
        super().update(viewport, scale)

        if self.touching:
            self.check_focus()
            self.check_click()


class VolumeSlider(Button):
    def __init__(
        self,
        surface: pygame.Surface,
        image: pygame.Surface,
        enabled: bool = True,
        action: gs | None = None,
        pos: tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__(surface, image, enabled, action, pos)


# class SliderKnob:
#     def __init__(self, surface: pygame.Surface, image: pygame.Surface, parent: Button, auto_pos: bool) -> None:
#         super().__init__(surface, image, auto_pos=auto_pos)

#         self.parent: Button = parent

#         self.left_bound: int = self.parent.pos[0]
#         self.right_bound: int = self.left_bound + self.parent.image.width

#         self.x_pos: int = self.left_bound
#         self.y_pos: int = self.parent.pos[1] + self.parent.image.height // 2

#         self.base_image: pygame.Surface = self.image
#         self.glow_image: pygame.Surface = self.create_hue(offset=40)
#         self.shadow_image: pygame.Surface = self.create_hue(offset=-40)

#     def update(self, viewport: pygame.Rect, scale: int) -> None:
#         mouse_pos: tuple[int, int] | None = self.scale_mouse(viewport=viewport, scale=scale)
#         if not mouse_pos or not self.parent.enabled:
#             return

#         touching: bool = self.image.get_rect(topleft=(self.x_pos, self.y_pos)).collidepoint(mouse_pos)
#         mouse_down: bool = pygame.mouse.get_pressed()[0]
#         mouse_up: bool = pygame.mouse.get_just_released()[0]

#         print(self.x_pos, self.y_pos)

#         if touching:
#             self.image = self.glow_image
#             print("touching")

#             if mouse_down:
#                 self.image = self.shadow_image
#                 self.x_pos = max(self.left_bound, min(mouse_pos[0], self.right_bound))

#         else:
#             self.image = self.base_image
