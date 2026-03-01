import pygame
from runtime.constants import MUSIC_PATH


class Sfx:

    def __init__(self) -> None:
        self.path: str = MUSIC_PATH

        self.hover_sfx: pygame.mixer.Sound = pygame.mixer.Sound(MUSIC_PATH + "hover_click.mp3")
        self.hover_sfx.set_volume(0.5)
        self.click_sfx: pygame.mixer.Sound = pygame.mixer.Sound(MUSIC_PATH + "click.mp3")

        self.jump_sfx: pygame.mixer.Sound = pygame.mixer.Sound(MUSIC_PATH + "footstep_one.mp3")

    def play(self):
        pygame.mixer.music.load(MUSIC_PATH + "8bit_canon.mp3")
        pygame.mixer.music.play(0)
