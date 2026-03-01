import pygame
from runtime.image import ImageManager, ButtonSprite
from runtime.constants import BUTTON_SCALAR, MENU_MARGIN, GameState as gs


class ButtonConfig:
    def __init__(self, surface: pygame.Surface, click_sfx: pygame.mixer.Sound, hover_sfx: pygame.mixer.Sound) -> None:
        self.surface: pygame.Surface = surface

        self.image: ImageManager = ImageManager(scalar=BUTTON_SCALAR)
        self.sprite: ButtonSprite = self.image.button

        self.click: pygame.mixer.Sound = click_sfx
        self.hover: pygame.mixer.Sound = hover_sfx

        self.main_buttons: list[Button] = [
            ActionButton(
                surface=self.surface, image=self.sprite.play, action=gs.PLAY, click_sfx=self.click, hover_sfx=self.hover
            ),
            ActionButton(
                surface=self.surface, image=self.sprite.quit, action=gs.QUIT, click_sfx=self.click, hover_sfx=self.hover
            ),
        ]

        self.settings_widget: Button = ActionButton(
            surface=self.surface,
            image=self.sprite.settings,
            action=gs.SETTINGS,
            pos=(self.surface.width - self.sprite.y_scalar - MENU_MARGIN, MENU_MARGIN),
            click_sfx=self.click,
            hover_sfx=self.hover,
        )

        self.settings_buttons: list[Button] = [
            ActionButton(
                surface=self.surface,
                image=self.sprite.menu,
                action=gs.MAIN_MENU,
                click_sfx=self.click,
                hover_sfx=self.hover,
            ),
            VolumeSlider(surface=self.surface, image=self.sprite.volume),
        ]

        self.pause_widget: Button = ActionButton(
            surface=self.surface,
            image=self.sprite.settings,
            action=gs.PAUSE,
            pos=(self.surface.width - self.sprite.y_scalar - MENU_MARGIN, MENU_MARGIN),
            click_sfx=self.click,
            hover_sfx=self.hover,
        )
        self.pause_buttons: list[Button] = [
            ActionButton(
                surface=self.surface,
                image=self.sprite.resume,
                action=gs.PLAY,
                click_sfx=self.click,
                hover_sfx=self.hover,
            ),
            ActionButton(
                surface=self.surface,
                image=self.sprite.menu,
                action=gs.MAIN_MENU,
                click_sfx=self.click,
                hover_sfx=self.hover,
            ),
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
        click_sfx: pygame.mixer.Sound | None = None,
        hover_sfx: pygame.mixer.Sound | None = None,
    ) -> None:
        self.surface: pygame.Surface = surface
        self.image: pygame.Surface = image
        self.enabled: bool = enabled
        self.action: gs | None = action
        self.pos: tuple[int, int] = pos
        self.click_sfx: pygame.mixer.Sound | None = click_sfx
        self.hover_sfx: pygame.mixer.Sound | None = hover_sfx

        self.pressed: bool = False
        self.mouse_pos: tuple[int, int] | None = None
        self.touching: bool = False
        self.mouse_down: bool = False
        self.mouse_up: bool = False

        self.base_image: pygame.Surface = self.image
        self.glow_image: pygame.Surface = self.create_hue(offset=40)
        self.shadow_image: pygame.Surface = self.create_hue(offset=-40)

    def scale_mouse(self, viewport: pygame.Rect, scale: int) -> tuple[int, int] | None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not viewport.collidepoint((mouse_x, mouse_y)):
            return None

        scale_x: int = (mouse_x - viewport.x) // scale
        scale_y: int = (mouse_y - viewport.y) // scale

        return scale_x, scale_y

    def create_hue(self, offset: int) -> pygame.Surface:
        hue: pygame.Surface = self.image.copy()
        if offset < 0:
            amount: int = abs(offset)
            hue.fill((amount, amount, amount), special_flags=pygame.BLEND_RGB_SUB)

        else:
            amount: int = offset
            hue.fill((amount, amount, amount), special_flags=pygame.BLEND_RGB_ADD)

        return hue

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        self.mouse_pos = self.scale_mouse(viewport=viewport, scale=scale)
        if not self.mouse_pos:
            return

        if not self.enabled:
            self.image = self.shadow_image
            return

        self.touching = self.image.get_rect(topleft=self.pos).collidepoint(self.mouse_pos)
        self.mouse_down = pygame.mouse.get_pressed()[0]
        self.mouse_up = pygame.mouse.get_just_released()[0]

    def draw(self) -> None:
        self.surface.blit(self.image, self.pos)


class ActionButton(Button):

    def __init__(
        self,
        surface: pygame.Surface,
        image: pygame.Surface,
        enabled: bool = True,
        action: gs | None = None,
        pos: tuple[int, int] = (0, 0),
        click_sfx: pygame.mixer.Sound | None = None,
        hover_sfx: pygame.mixer.Sound | None = None,
    ) -> None:
        super().__init__(surface, image, enabled, action, pos, click_sfx, hover_sfx)

        self.hover_toggle: bool = True

    def update(self, viewport: pygame.Rect, scale: int):
        super().update(viewport, scale)

        if self.touching:
            self.image = self.glow_image

            if self.hover_sfx and self.hover_toggle:
                self.hover_sfx.play()
                self.hover_toggle = False

            if self.mouse_down:
                self.image = self.shadow_image

            elif self.mouse_up:
                self.pressed = True

                if self.click_sfx:
                    self.click_sfx.play()

        else:
            self.image = self.base_image
            self.pressed = False
            self.hover_toggle = True


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
