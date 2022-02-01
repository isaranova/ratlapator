import os
from flask import Flask, render_template, request
from config import Config
from form import RatForm

from src.canvas import Canvas

app = Flask(__name__)
app.config.from_object(Config)
save_path = os.path.join('static', 'ref1.png')


@app.route('/',  methods=['GET', 'POST'])
def index():
    form = RatForm()
    canvas = Canvas(1000, 1000)
    form.validate_on_submit()
    if request.method == 'POST':
        crop_box = [form.width.data, form.height.data]
        colors = {
            'Green': [(0, 128, 0), form.color.green.data],
            'Lime': [(0, 255, 0), form.color.lime.data],
            'Olive': [(128, 128, 0), form.color.olive.data],
            'Yellow': [(255, 255, 0), form.color.yellow.data],

            'Black': [(0, 0, 0), form.color.black.data],
            'Orange': [(255, 165, 0), form.color.orange.data],
            'Pink': [(255, 105, 180), form.color.pink.data],
            'Brown': [(139, 69, 19), form.color.brown.data],

            'Maroon': [(128, 0, 0), form.color.maroon.data],
            'Red': [(255, 0, 0), form.color.red.data],
            'Purple': [(128, 0, 128), form.color.purple.data],
            'Magenta': [(255, 0, 255), form.color.magenta.data],

            'Navy': [(0, 0, 128), form.color.navy.data],
            'Blue': [(0, 0, 255), form.color.blue.data],
            'Teal': [(0, 128, 128), form.color.teal.data],
            'Cyan': [(0, 255, 255), form.color.cyan.data]
        }
        color_amounts = {
            values[0] + tuple([255]): values[1] for color_name, values in colors.items() if values[1] != 0
        }
        canvas.add_rat(color_amounts, form.speed.data, form.size.data / 10)
        canvas.print_rats()
        canvas.save_canvas_with_crop_box(save_path=save_path)

    return render_template('main.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
