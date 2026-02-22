import pygame

pygame.init()


class Image:

    def __init__(self, scalar: int) -> None:
        self.scalar: int = scalar
        self.img_path: str = "assets/images/"

    def boat_img(self) -> pygame.Surface:
        boat_img: pygame.Surface = pygame.image.load(self.img_path + "Boat.png")
        boat_img = pygame.transform.scale_by(boat_img, 3)
        return boat_img

    def play_button(self) -> pygame.Surface:
        play_img: pygame.Surface = pygame.image.load(self.img_path + "play.png")
        play_img = pygame.transform.scale_by(play_img, self.scalar)
        return play_img

    def quit_button(self):
        quit_img: pygame.Surface = pygame.image.load(self.img_path + "quit.png")
        quit_img = pygame.transform.scale_by(quit_img, self.scalar)
        return quit_img
