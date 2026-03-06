import pygame
from runtime.constants import MUSIC_PATH


class Sfx:

    def __init__(self) -> None:
        self.path: str = MUSIC_PATH
        self.audio_state: AudioState = AudioState(volume=50)

        self.hover_sfx: pygame.mixer.Sound = pygame.mixer.Sound(MUSIC_PATH + "hover_click.mp3")
        self.hover_sfx.set_volume(0.5)
        self.click_sfx: pygame.mixer.Sound = pygame.mixer.Sound(MUSIC_PATH + "click.mp3")
        self.click_sfx.set_volume(0.5)
        self.swoosh_sfx: pygame.mixer.Sound = pygame.mixer.Sound(MUSIC_PATH + "swoosh.mp3")
        self.swoosh_sfx.set_volume(0.2)

        self.log_sfx: list[pygame.mixer.Sound] = [
            pygame.mixer.Sound(MUSIC_PATH + "footstep_one.mp3"),
            pygame.mixer.Sound(MUSIC_PATH + "footstep_two.mp3"),
            pygame.mixer.Sound(MUSIC_PATH + "footstep_three.mp3"),
        ]

        self.grass_sfx: list[pygame.mixer.Sound] = [
            pygame.mixer.Sound(MUSIC_PATH + "grass_one.mp3"),
            pygame.mixer.Sound(MUSIC_PATH + "grass_two.mp3"),
            pygame.mixer.Sound(MUSIC_PATH + "grass_three.mp3"),
        ]

        self.update_volume()

    def update_volume(self):
        converted_volume: float = self.audio_state.volume / 100

        self.hover_sfx.set_volume(converted_volume)
        self.click_sfx.set_volume(converted_volume)
        self.swoosh_sfx.set_volume(converted_volume)
        for sound in self.log_sfx + self.grass_sfx:
            sound.set_volume(converted_volume)


class AudioState:
    def __init__(self, volume: int = 50) -> None:
        self.volume: int = max(0, min(100, volume))

    def set_volume(self, value: int) -> None:
        self.volume: int = max(0, min(100, value))
