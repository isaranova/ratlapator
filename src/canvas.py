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

    def add_rat(self, color_amounts, speed, size):
        """
        Adds rat painter to the canvas.

        :param color_amounts: dict of color as RGBA tuple and int amount from 0 to 255
        :param speed: rat's speed, from 1 to 5
        :param size: rat's size, from 0.5 to 1.5
        """
        rat = VisualRat(color_amounts, speed, size, self.frame_size)
        self.rats.append(rat)

    def reset_rats(self):
        self.rats = list()

    def print_rats(self):
        for rat in self.rats:
            pawprints = rat.get_pawprints()
            for pawprint in pawprints:
                maybe_not = randint(0, 100)
                if maybe_not > 100:
                    continue

                self.canvas.paste(pawprint[0], pawprint[1], pawprint[0])

            # dot = Image.open('img\\dot.png')
            # self.canvas.paste(dot, self.rats[0].rat.direction, dot)

    def move_rats(self):
        for rat in self.rats:
            rat.do_rat_step()
        self.number += 1

    def get_crop_box_bounds(self, crop_box=None):
        if not crop_box:
            crop_box = self.frame_size

        center = [self.frame_size[0] // 2, self.frame_size[1] // 2]

        bounds = [
            (int(center[0] - crop_box[0] / 2), int(center[1] - crop_box[1] / 2)),
            (int(center[0] + crop_box[0] / 2), int(center[1] + crop_box[1] / 2))
        ]

        return bounds

    def get_encoded_img(self):
        buffered = BytesIO()
        to_be_saved = self.canvas.copy()
        to_be_saved.save(buffered, format="PNG")
        encoded = base64.b64encode(buffered.getvalue())
        return encoded

    def save_canvas_with_crop_box(self, save_path, crop_box=None):
        bounds = self.get_crop_box_bounds(crop_box)
        output_canvas = self.canvas.copy()
        img1 = ImageDraw.Draw(output_canvas)
        img1.rectangle(bounds, outline='red')

        output_canvas.save(save_path)

    def save_cropped(self, crop_box=None):
        box = self.get_crop_box_bounds(crop_box)
        box = box[0] + box[1]
        cropped = self.canvas.copy().crop(box)
        cropped.save(f'img\\cropped{self.number}.png')

    def reset_canvas(self):
        self.canvas = Image.new('RGBA', tuple(self.frame_size), 'white')
        self.rats = []
        self.number = 0