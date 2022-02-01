import math
from random import randint
from math import cos, sin, radians

import numpy as np
from . import config


class Rat:
    def __init__(self, color_amounts, speed, size, frame_size):
        self._set_color_amount(color_amounts)  # dictionary with color str and amount float
        self.speed = speed
        self.size = size  # medium rat = 1
        self.frame_size = frame_size

        self.paws_distance = self.size * config.MEDIUM_RAT_SIZE_PAW_DISTANCE
        self.tail_distance = (
                self.size * config.MEDIUM_RAT_SIZE_PAW_DISTANCE * config.PAW_TAIL_DISTANCE_RATIO
        )

        self._init_position()
        self._init_direction()

    def _init_position(self):
        self.x = randint(0, self.frame_size[0])
        self.y = randint(0, self.frame_size[1])

    def _set_position(self, x, y):
        self.x = x if x < self.frame_size[0] else self.frame_size[0] - 1
        self.y = y if y < self.frame_size[1] else self.frame_size[1] - 1

    def _init_direction(self):
        corners = [
            [0, 0], [self.frame_size[0], self.frame_size[1]],
            [self.frame_size[0] // 2, self.frame_size[1]],
            [self.frame_size[0], self.frame_size[1] // 2],
            [self.frame_size[0], 0], [0, self.frame_size[1]],
            [self.frame_size[0] // 2, 0], [0, self.frame_size[1] // 2]
        ]

        distances = [math.dist([self.x, self.y], corner) for corner in corners]
        max_distance = max(distances)
        max_distance_id = distances.index(max_distance)
        self.direction = corners[max_distance_id]
        self.direction_timer = randint(2, 4)  # 2-10 rat steps until change of direction

    def _set_color_amount(self, color_amounts):
        self.color_amounts = dict()
        for color, amount in color_amounts.items():
            self.color_amounts[color] = amount

    def get_color_amount(self, color):
        return self.color_amounts[color]

    def lower_color_amount(self, ratio):
        for color, amount in self.color_amounts.items():
            self.color_amounts[color] = amount // ratio

    def get_position(self, distance, angle):
        rad = radians(angle)
        x = self.x + (distance * cos(rad))
        y = self.y + (distance * sin(rad))

        return [round(x), round(y)]

    def rotate(self, origin, points, angle):
        rotated = []
        angle = radians(angle)
        cosin = math.cos(angle)
        sinus = math.sin(angle)

        for point in points:
            ox, oy = origin
            px, py = point

            qx = ox + cosin * (px - ox) - sinus * (py - oy)
            qy = oy + sinus * (px - ox) + cosin * (py - oy)

            rotated.append([qx, qy])

        return rotated
    
    @staticmethod
    def get_tail_wiggle_angle():
        return randint(config.TAIL_ANGLE - 12, config.TAIL_ANGLE + 12)

    def get_body_positions(self):
        horizontal_vec = self.get_horizontal_vec()
        angle = self.get_rotation_angle(horizontal_vec)

        if self.direction[1] > self.y:
            angle = 360 - angle
            
        left_front = self.get_position(self.paws_distance, config.LEFT_FRONT_ANGLE)
        right_front = self.get_position(self.paws_distance, config.RIGHT_FRONT_ANGLE)
        left_back = self.get_position(self.paws_distance, config.LEFT_BACK_ANGLE)
        right_back = self.get_position(self.paws_distance, config.RIGHT_BACK_ANGLE)
        tail = self.get_position(self.tail_distance, self.get_tail_wiggle_angle())

        positions = [left_front, right_front, left_back, right_back, tail]
        positions = self.rotate([self.x, self.y], positions, 360 - angle)
        positions = [(int(position[0]), int(position[1])) for position in positions]

        return positions

    @staticmethod
    def get_vector_from_two_points(start, end):
        return tuple([end[0] - start[0], end[1] - start[1]])

    @staticmethod
    def get_angle_between_vectors(vec1, vec2):
        unit_vector_1 = vec1 / np.linalg.norm(vec1)
        unit_vector_2 = vec2 / np.linalg.norm(vec2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)
        angle = np.rad2deg(angle)
        return angle

    def get_rotation_angle(self, ref_vec):
        direction_vec = self.get_vector_from_two_points([self.x, self.y], self.direction)
        angle = self.get_angle_between_vectors(direction_vec, ref_vec)
        return angle

    def get_vertical_vec(self, center):
        return self.get_vector_from_two_points(center, [center[0], center[1] - 42])

    def get_horizontal_vec(self):
        return self.get_vector_from_two_points([self.x, self.y], [self.x + 42, self.y])

    def move(self):
        if self.direction_timer <= 0:
            self._init_direction()

        horizontal_vec = self.get_horizontal_vec()
        angle = self.get_rotation_angle(horizontal_vec)

        if self.direction[1] > self.y:
            angle = 360 - angle

        new_position = self.get_position(self.tail_distance, 360 - angle)
        self._set_position(*new_position)
        self.direction_timer -= 1 * self.speed  # speed is from 1 to 5
        self.lower_color_amount(2)
