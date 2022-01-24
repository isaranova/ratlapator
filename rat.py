from random import randint
from math import cos, sin, radians

import config


class Rat:
    def __init__(self, colors, color_amount, speed, size, frame_size):
        self.colors = colors
        self.color_amount = color_amount
        self.speed = speed
        self.size = size  # medium rat = 1
        self.frame_size = frame_size

        self._init_position()

    def _init_position(self):
        self.x = randint(0, self.frame_size[0])
        self.y = randint(0, self.frame_size[1])
        self.direction = [randint(0, self.frame_size[0]), randint(0, self.frame_size[1])]

        self.paws_distance = self.size * config.MEDIUM_RAT_SIZE_PAW_DISTANCE
        self.tail_distance = (
                self.size * config.MEDIUM_RAT_SIZE_PAW_DISTANCE * config.PAW_TAIL_DISTANCE_RATIO
        )

    def get_position(self, distance, angle):
        rad = radians(angle)
        x = self.x + (distance * cos(rad))
        y = self.y + (distance * sin(rad))

        return [round(x), round(y)]

    def get_body_position(self):
        positions = {
            'left_front': self.get_position(self.paws_distance, config.LEFT_FRONT_ANGLE),
            'right_front': self.get_position(self.paws_distance, config.RIGHT_FRONT_ANGLE),
            'left_back': self.get_position(self.paws_distance, config.LEFT_BACK_ANGLE),
            'right_back': self.get_position(self.paws_distance, config.RIGHT_BACK_ANGLE),
            'tail': self.get_position(self.tail_distance, config.TAIL_ANGLE)
        }
