from flask import Flask, render_template
from config import Config
from form import RatForm

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/index')
def index():
    form = RatForm()
    return render_template('main.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
