from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, ValidationError


class LoginForm(Form):
    first_name = StringField('first_name', validators=[InputRequired(message=None)])
    last_name = StringField('last_name', validators=[InputRequired(message=None)])
    id_num = StringField('id_num', validators=[InputRequired(message=None)])

    def validate_id_num(form, field):
        if not str(field.data).isdigit():
            raise ValidationError('Field must be numeric')
