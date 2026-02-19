from game.constants import THRESHOLD_MULTIPLIER, EASING_MULTIPLIER


class Camera:
    def __init__(self, player_y: float, grid_constant: int) -> None:
        self.initial_y: float = player_y
        self.grid_constant: int = grid_constant

        self.threshold: float = self.initial_y - self.grid_constant * THRESHOLD_MULTIPLIER
        self.y_offset: float = 0

    def get_offset(self, new_player_y: float, delta_time: float) -> float:
        easing_speed: float = delta_time * EASING_MULTIPLIER

        self.y_offset = (self.threshold - new_player_y) * easing_speed
        return self.y_offset
