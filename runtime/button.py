import pygame
from runtime.image import ImageManager, ButtonSprite
from runtime.constants import BUTTON_SCALAR, MENU_MARGIN, SCALED_SLIDER_LENGTH, SCALED_SLIDER_START_X, GameState as gs


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
            VolumeSlider(surface=self.surface, image=self.sprite.volume, knob_image=self.sprite.knob),
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
            VolumeSlider(surface=self.surface, image=self.sprite.volume, knob_image=self.sprite.knob),
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

    def check_for_click(self) -> None:
        mouse_down: bool = pygame.mouse.get_pressed()[0]
        mouse_up: bool = pygame.mouse.get_just_released()[0]

        if mouse_down:
            self.display_image = self.shadow_image

        elif mouse_up:
            self.clicked = True

    def check_for_focus(self) -> None:
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

    def prep_state(self) -> None:
        self.clicked = False
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

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        super().update(viewport, scale)

        if self.touching:
            self.check_for_focus()
            self.check_for_click()

        else:
            self.prep_state()


class VolumeSlider(Button):
    def __init__(
        self,
        surface: pygame.Surface,
        image: pygame.Surface,
        knob_image: pygame.Surface,
        enabled: bool = True,
        action: gs | None = None,
        pos: tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__(surface, image, enabled, action, pos)

        self.knob_image: pygame.Surface = knob_image
        self.x_range: int = SCALED_SLIDER_LENGTH
        self.volume: int = 50
        self.set_volume: bool = False
        self.knob: SliderKnob = SliderKnob(surface=self.surface, image=self.knob_image, x_range=self.x_range)

    def get_knob_pos(self) -> tuple[int, int]:
        x: int = self.pos[0] + SCALED_SLIDER_START_X
        y: int = self.pos[1] + (self.display_image.height - self.knob.display_image.height) // 2
        return x, y

    def sync_volume(self, volume: int) -> None:
        clamped: int = max(0, min(100, volume))
        if self.volume == clamped:
            return

        self.volume = clamped
        self.knob.volume = clamped
        self.knob.set_volume_position()

    def mouse_in_range(self) -> bool:
        if self.mouse_pos:
            in_x_range: bool = (self.knob.start_pos[0] + self.x_range) >= self.mouse_pos[0] >= self.knob.start_pos[0]
            in_y_range: bool = self.pos[1] <= self.mouse_pos[1] <= (self.pos[1] + self.display_image.height)
            return True if in_x_range and in_y_range else False

        return False

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        super().update(viewport, scale)
        if self.knob.start_pos == (0, 0):
            self.knob.start_pos = self.get_knob_pos()
            self.knob.volume = self.volume
            self.knob.set_volume_position()

        self.knob.mouse_in_range = self.mouse_in_range()
        self.knob.update(viewport=viewport, scale=scale)

        self.set_volume = self.knob.set_volume
        self.volume = self.knob.volume

    def draw(self) -> None:
        super().draw()
        self.knob.draw()


class SliderKnob(Button):
    def __init__(
        self,
        surface: pygame.Surface,
        image: pygame.Surface,
        enabled: bool = True,
        action: gs | None = None,
        pos: tuple[int, int] = (0, 0),
        x_range: int = 0,
    ) -> None:
        super().__init__(surface, image, enabled, action, pos)
        self.x_range: int = x_range
        self.start_pos: tuple[int, int] = pos
        self.volume: int = 50
        self.set_volume: bool = False

        self.mouse_in_range: bool = False

    def update(self, viewport: pygame.Rect, scale: int) -> None:
        super().update(viewport, scale)
        if self.touching:
            self.check_for_focus()

        else:
            self.prep_state()

        self.check_for_drag()

    def check_for_drag(self) -> None:
        mouse_down: bool = pygame.mouse.get_pressed()[0]
        self.set_volume = False

        if mouse_down and self.mouse_in_range:
            self.display_image = self.shadow_image
            self.pos = (self.mouse_pos[0] - self.display_image.width // 2 if self.mouse_pos else 0, self.start_pos[1])
            self.check_range()
            self.update_volume()
        else:
            self.check_range()

    def update_volume(self) -> None:
        self.volume = int(((self.pos[0] - self.start_pos[0]) / self.x_range) * 100)
        self.set_volume = True

    def set_volume_position(self) -> None:
        if self.start_pos == (0, 0):
            return
        self.pos = int((self.volume / 100) * self.x_range + self.start_pos[0]), self.start_pos[1]

    def check_range(self) -> None:
        if self.pos[0] < self.start_pos[0]:
            self.pos = self.start_pos

        elif self.pos[0] > self.start_pos[0] + self.x_range:
            self.pos = self.start_pos[0] + self.x_range, self.start_pos[1]
