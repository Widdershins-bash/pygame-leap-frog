import pygame

pygame.init()


class Image:

    def __init__(self, scaler: float = 3) -> None:
        self.scaler: float = scaler

        self.boat_img = self.get_boat_img()

    def get_boat_img(self) -> pygame.Surface:
        boat_img: pygame.Surface = pygame.image.load("assets/images/Boat.png")
        boat_img = pygame.transform.scale_by(boat_img, self.scaler)

        return boat_img
