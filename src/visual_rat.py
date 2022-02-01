import os
from random import randint
from pathos.multiprocessing import ProcessingPool

from PIL import Image, ImageFilter, ImageChops
import numpy as np

from src.rat import Rat


class VisualRat:
    def __init__(self, color_amounts, speed, size, frame_size):
        self.rat = Rat(color_amounts, speed, size, frame_size)
        self.frame_size = frame_size
        self.rat_size = size
        self.current_folder = os.path.abspath(os.path.curdir)

        self.left_front_path = os.path.join('static', 'left-front-pawprint.png')
        self.right_front_path = os.path.join('static', 'right-front-pawprint.png')
        self.left_back_path = os.path.join('static', 'left-back-pawprint.png')
        self.right_back_path = os.path.join('static', 'right-back-pawprint.png')
        self.tail_path = os.path.join('static', 'tail.png')

    def pick_color(self):
        amounts_sum = sum(self.rat.color_amounts.values())

        number = randint(0, amounts_sum)
        prev_sum = 0
        for color, amounts in self.rat.color_amounts.items():
            prev_sum += amounts
            if number <= prev_sum:
                return color

        return self.rat.color_amounts.keys()[0]

    @staticmethod
    def white_to_transparency_gradient(img):
        x = np.asarray(img.convert('RGBA')).copy()
        x[:, :, 3] = (255 - x[:, :, :3].mean(axis=2)).astype(np.uint8)
        return Image.fromarray(x)

    def color_image(self, im, color):
        im = im.convert('RGBA')

        data = np.array(im)  # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        # Replace white with red... (leaves alpha values alone...)
        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[...][white_areas.T] = (0, 0, 0, 0)  # Transpose back needed
        to_color_areas = (alpha != 0)
        data[...][to_color_areas.T] = color

        im2 = Image.fromarray(data)
        return im2

    def get_mask(self, image, ref_name, ref_count, ref_type):
        image_size = image.size
        number = randint(1, ref_count)
        ref_path = f'{ref_name}{number}.{ref_type}'
        ref_path = os.path.join('static', ref_path)

        mask = Image.open(ref_path).convert('RGBA')
        angle = randint(0, 360)
        mask = mask.rotate(angle)
        mask = mask.resize((image_size[0] * 2, image_size[1] * 2))
        bbox = (
            mask.size[0] // 4,  # left
            mask.size[1] // 4,  # top
            mask.size[0] // 4 * 3,  # right
            mask.size[1] // 4 * 3   # bottom
        )
        mask = mask.crop(bbox)
        mask = mask.resize(image_size)
        mask = Image.composite(mask, image, image)
        return mask

    def get_pawprint(self, img_path, position):
        image_original = Image.open(img_path)
        image = image_original.copy()

        # blobs
        blob_prob = randint(0, 100)
        if blob_prob > 30 or 'tail' in img_path:
            image = self.get_mask(image, 'blob', 5, 'png')

        # rotate
        vertical_vec = self.rat.get_vertical_vec(position)
        angle = self.rat.get_rotation_angle(vertical_vec)

        if position[0] < self.rat.direction[0]:
            angle = 360 - angle

        if 'tail' in img_path:
            angle += 180

        angle = randint(int(angle) - 15, int(angle) + 15)
        image = image.rotate(angle, expand=True, fillcolor=(255, 255, 255, 0))

        # color and transparency
        color = self.pick_color()
        transparency = self.rat.get_color_amount(color)
        image = self.color_image(image, (color[0], color[1], color[2], transparency))
        cloud_mask = self.get_mask(image, 'clouds', 4, 'jpg')
        image = ImageChops.add(image, cloud_mask, scale=2.0)
        image = image.filter(ImageFilter.MedianFilter(size=3))

        # blur
        blurriness = randint(0, 5)
        if blurriness:
            image = image.filter(ImageFilter.GaussianBlur(radius=blurriness))

        return image

    def image_size_and_position_optimalization(self, image, position, back_paws=False, tail=False):
        # rat size is from 0.5 to 1.5
        if tail:
            image = image.resize(
                (int((self.frame_size[0] // 4) * self.rat_size), int((self.frame_size[1] // 4) * self.rat_size))
            )
        elif back_paws:
            image = image.resize(
                (int((self.frame_size[0] // 10) * self.rat_size), int((self.frame_size[1] // 10) * self.rat_size))
            )
        else:
            image = image.resize(
                (int((self.frame_size[0] // 15) * self.rat_size), int((self.frame_size[1] // 15) * self.rat_size))
            )
        lefttop_corner = (position[0] - image.size[0] // 2, position[1] - image.size[1] // 2)
        return [image, lefttop_corner]

    def pool_optimalization(self, input):
        img_path, position = input
        pawprint = self.get_pawprint(img_path, position)
        optimized_pawprint = self.image_size_and_position_optimalization(
            pawprint,
            position,
            back_paws='back' in img_path,
            tail='tail' in img_path
        )
        return optimized_pawprint

    def get_pawprints(self):
        positions = self.rat.get_body_positions()

        pool_list = [
            [self.left_front_path, positions[0]],
            [self.right_front_path, positions[1]],
            [self.left_back_path, positions[2]],
            [self.right_back_path, positions[3]],
            [self.tail_path, positions[4]]
        ]

        with ProcessingPool(5) as pool:
            pawprints = pool.map(self.pool_optimalization, pool_list)

        return pawprints

    def do_rat_step(self):
        self.rat.move()
