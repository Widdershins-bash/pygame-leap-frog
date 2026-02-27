import pygame
from runtime.image import ImageManager
from runtime.constants import BUTTON_SCALAR, MENU_MARGIN, GameState as gs


class ButtonConfig:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface: pygame.Surface = surface

        self.image: ImageManager = ImageManager(scalar=BUTTON_SCALAR)
        self.button = self.image.button

        self.main_buttons: list[Button] = [
            Button(surface=self.surface, image=self.button.play, action=gs.PLAY),
            Button(surface=self.surface, image=self.button.quit, action=gs.QUIT),
        ]

        self.settings_widget: Button = Button(
            surface=self.surface,
            image=self.button.settings,
            action=gs.SETTINGS,
            pos=(self.surface.width - self.button.y_scalar - MENU_MARGIN, MENU_MARGIN),
        )
        self.settings_buttons: list[Button] = [
            Button(surface=self.surface, image=self.button.resume, action=gs.PLAY),
            Button(surface=self.surface, image=self.button.menu, action=gs.MAIN_MENU),
            Button(surface=self.surface, image=self.button.volume, action="TBD"),
        ]


class Button:
    def __init__(
        self, surface: pygame.Surface, image: pygame.Surface, action: str, pos: tuple[int, int] = (0, 0)
    ) -> None:
        self.surface: pygame.Surface = surface
        self.image: pygame.Surface = image
        self.action: str = action
        self.pos: tuple[int, int] = pos

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

    def draw(self) -> None:
        self.surface.blit(self.image, self.pos)
