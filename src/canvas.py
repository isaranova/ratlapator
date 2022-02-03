from random import randint
from PIL import Image, ImageDraw
import base64
from io import BytesIO

from src.visual_rat import VisualRat


class Canvas:
    def __init__(self, size_x, size_y):
        self.frame_size = [size_x, size_y]
        self.canvas = Image.new('RGBA', tuple(self.frame_size), 'white')
        self.rats = list()
        self.number = 0

    def add_rat(self, color_amounts, speed, size, x=None, y=None, direction=None, direction_timer=None):
        """
        Adds rat painter to the canvas.

        :param color_amounts: dict of color as RGBA tuple and int amount from 0 to 255
        :param speed: rat's speed, from 1 to 5
        :param size: rat's size, from 0.5 to 1.5
        """
        rat = VisualRat(color_amounts, speed, size, self.frame_size, x, y, direction, direction_timer)
        self.rats.append(rat)

    def reset_rats(self):
        self.rats = list()

    def get_rat_speed_size(self):
        # only for one rat atm
        return [self.rats[0].rat.speed, self.rats[0].rat.size]

    def get_rat_position_direction(self):
        # only for one rat atm
        return [self.rats[0].rat.x, self.rats[0].rat.y, self.rats[0].rat.direction, self.rats[0].rat.direction_timer]

    def print_rats(self):
        for rat in self.rats:
            pawprints = rat.get_pawprints()
            for pawprint in pawprints:
                maybe_not = randint(0, 100)
                if maybe_not > 100:
                    continue

                self.canvas.paste(pawprint[0], pawprint[1], pawprint[0])

    def move_rats(self):
        for rat in self.rats:
            rat.do_rat_step()
        self.number += 1

    def get_color_amounts(self):
        # only for one rat atm
        return self.rats[0].rat.color_amounts

    def get_encoded_img(self):
        buffered = BytesIO()
        to_be_saved = self.canvas.copy()
        to_be_saved.save(buffered, format="PNG")
        encoded = base64.b64encode(buffered.getvalue())
        return encoded

    def set_canvas_from_encoded_img(self, data):
        data = data.replace('data:image/png;base64', '')
        self.canvas = Image.open(BytesIO(base64.b64decode(data)))

    def reset_canvas(self):
        self.canvas = Image.new('RGBA', tuple(self.frame_size), 'white')
        self.rats = []
        self.number = 0
