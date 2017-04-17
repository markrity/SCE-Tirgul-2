from flask_babel import gettext
from flask_wtf import Form, validators
from wtforms import StringField, BooleanField, TextField
from wtforms.validators import DataRequired, InputRequired


class LoginForm(Form):
    first_name = StringField('first_name', validators=[InputRequired(message=None)])
    last_name = StringField('last_name', validators=[InputRequired(message=None)])
    id_num = StringField('id_num', validators=[InputRequired(message=None)])