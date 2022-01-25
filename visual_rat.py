import os
from random import randint

from PIL import Image

from rat import Rat


class VisualRat:
    def __init__(self, color_amounts, speed, size, frame_size):
        self.rat = Rat(color_amounts, speed, size, frame_size)
        self.left_front_path = os.path.join('img', 'left-front-pawprint.png')
        self.right_front_path = os.path.join('img', 'right-front-pawprint.png')
        self.left_back_path = os.path.join('img', 'left-back-pawprint.png')
        self.right_back_path = os.path.join('img', 'right-back-pawprint.png')
        self.tail_path = os.path.join('img', 'tail.png')

    def get_pawprint(self, img_path):
        image_original = Image.open(img_path)
        image = image_original.copy()
        # blobs


        # rotate
        vertical_vec =  self.rat.get_vertical_vec()
        angle = self.rat.get_rotation_angle(vertical_vec)

        if self.rat.x > self.rat.direction[0]:
            angle = 360 - angle

        angle = randint(int(angle) - 15, int(angle) + 15)
        image.rotate(angle)

        # smear
        # color
        # transparency
        return image

    def get_pawprints(self):
        positions = self.rat.get_body_positions()

        left_front = [self.get_pawprint(self.left_front_path), positions['left-front']]
        right_front = [self.get_pawprint(self.right_front_path), positions['right_front']]
        left_back = [self.get_pawprint(self.left_back_path), positions['left-back']]
        right_back = [self.get_pawprint(self.right_back_path), positions['right-back']]
        tail = [self.get_pawprint(self.tail_path),  positions['tail']]

        pawprints = {
            'left_front': left_front,
            'right_front': right_front,
            'left_back': left_back,
            'right_back': right_back,
            'tail': tail
        }

        return pawprints


class Canvas:
    def __init__(self, size_x, size_y):
        self.frame_size = [size_x, size_y]
        self.canvas = Image.new('RGBA', tuple(self.frame_size), 'white')
        self.rats = list()

    def add_rat(self, color_amounts, speed, size):
        rat = VisualRat(color_amounts, speed, size, self.frame_size)
        self.rats.append(rat)

    def print_rats(self):
        for rat in self.rats:
            pass
