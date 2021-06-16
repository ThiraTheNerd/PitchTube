from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError,TextAreaField
from wtforms.validators import Required, Email, EqualTo
from ..models import User

class UpdateProfile(FlaskForm):
  bio = TextAreaField('Tell us more about yourself', validators=[Required()])
  submit = SubmitField('Submit')