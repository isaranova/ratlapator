import os
from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from config import Config
from form import RatForm

from src.canvas import Canvas

app = Flask(__name__)
app.config.from_object(Config)
save_path = os.path.join('static', 'ref1.png')
CSRFProtect(app)


steps_counter = 0
canvas = Canvas(1000, 800)


def get_img_string():
    global canvas
    img = canvas.get_encoded_img()
    string_img = f"data:image/png;base64,{img.decode()}"
    return string_img


@app.route('/',  methods=['GET', 'POST'])
def index():
    global steps_counter
    global canvas
    form = RatForm()

    if (request.method == "POST" and steps_counter > 0) or (request.get_json() and 'reset' in request.get_json()):
        if 'reset' in request.get_json():
            canvas.reset_canvas()
            steps_counter = 0
        else:
            canvas.move_rats()
            canvas.print_rats()
            steps_counter -= 1
            print(steps_counter)
            print(canvas.rats[0].rat.color_amounts)
        results = {
            'image': get_img_string(),
            'steps': steps_counter,
        }
        return jsonify(results)

    elif form.validate_on_submit():
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
            'Blue': [(0, 0, 255), form.color.blue.data]
        }
        color_amounts = {
            values[0] + tuple([255]): values[1] for color_name, values in colors.items() if values[1] != 0
        }

        if not color_amounts:
            return render_template('main.html', form=form, image_name=get_img_string(), no_color=True, steps=0)

        canvas.reset_rats()
        steps_counter = form.steps.data
        canvas.add_rat(color_amounts, form.speed.data, form.size.data / 10)
        canvas.print_rats()
        return render_template('main.html', form=form, image_name=get_img_string(), no_color=False, steps=steps_counter)

    return render_template('main.html', form=form, image_name=get_img_string(), no_color=False, steps=0)


if __name__ == "__main__":
    app.run(debug=True)
