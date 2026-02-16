import pygame


class Screen:
    def __init__(self, logical_size: int, player_size: int, margin: int, font: pygame.Font) -> None:
        self.logical_size: int = logical_size
        self.player_size: int = player_size
        self.margin: int = margin
        self.font: pygame.Font = font

        self.fullscreen: bool = False
        self.screen: pygame.Surface = pygame.display.set_mode((self.logical_size, self.logical_size), pygame.RESIZABLE)
        self.logical: pygame.Surface = pygame.Surface((self.logical_size, self.logical_size))

    def check_state(self) -> bool:

        if not self.fullscreen:
            note_render: pygame.Surface = self.font.render("Press F for Fullscreen", False, "black")
            self.logical.blit(
                note_render,
                (
                    (self.logical_size - note_render.width) // 2,
                    self.player_size + (self.player_size - note_render.height) // 2,
                ),
            )

        for event in pygame.event.get():
            running = event.type != pygame.QUIT

            if event.type == pygame.KEYDOWN:
                running = event.key != pygame.K_ESCAPE or fullscreen

                if event.key == pygame.K_f:
                    if fullscreen:
                        self.screen = pygame.display.set_mode((self.logical_size, self.logical_size), pygame.RESIZABLE)

                    else:
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    fullscreen = not fullscreen

        return running

    def flip(self):

        scalar: int = max(1, min(self.screen.width, self.screen.height) // self.logical_size)
        logical_transform: pygame.Surface = pygame.transform.scale(
            self.logical, (self.logical_size * scalar, self.logical_size * scalar)
        )
        self.screen.blit(
            logical_transform,
            ((self.screen.width - logical_transform.width) // 2, (self.screen.height - logical_transform.height) // 2),
        )
        pygame.display.flip()
