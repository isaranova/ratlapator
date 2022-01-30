from flask_wtf import FlaskForm
from wtforms import FormField, IntegerField, IntegerRangeField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, NumberRange


COLORS = {
    'Green': (0, 128, 0),
    'Lime': (0, 255, 0),
    'Olive': (128, 128, 0),
    'Yellow': (255, 255, 0),

    'Black': (0, 0, 0),
    'Orange': (255, 165, 0),
    'Pink': (255, 105, 180),
    'Brown': (139, 69, 19),

    'Maroon': (128, 0, 0),
    'Red': (255, 0, 0),
    'Purple': (128, 0, 128),
    'Magenta': (255, 0, 255),

    'Navy': (0, 0, 128),
    'Blue': (0, 0, 255),
    'Teal': (0, 128, 128),
    'Cyan': (0, 255, 255),
}


class ColorForm(FlaskForm):
    black = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    navy = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    teal = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    green = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)

    brown = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    blue = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    cyan = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    lime = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)

    purple = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    red = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    maroon = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    olive = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)

    magenta = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    pink = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    orange = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)
    yellow = IntegerField(validators=[NumberRange(min=0, max=255)], default=0)


class RatForm(FlaskForm):
    color = FormField(ColorForm)

    speed = IntegerRangeField(validators=[NumberRange(min=1, max=5)], default=3)
    size = IntegerRangeField(validators=[NumberRange(min=50, max=150)], default=100)
    steps = IntegerRangeField(validators=[NumberRange(min=1, max=10)], default=5)

    width = IntegerField()
    height = IntegerField()

    submit = SubmitField()
