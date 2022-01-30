"""
from canvas import Canvas

if __name__ == '__main__':
    blue = (0, 0, 255, 255)
    green = (0, 255, 0, 255)
    red = (255, 0, 0, 255)

    canvas = Canvas(800, 800)
    crop_box = [400, 300]

    canvas.add_rat({blue: 250, green: 140, red: 255}, 5, 1.5)
    canvas.print_rats()

    for _ in range(4):
        canvas.move_rats()
        canvas.print_rats()
        canvas.show_canvas_with_crop_box(crop_box)
"""