from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError,TextAreaField,SelectField
from wtforms.validators import Required, Email, EqualTo
from ..models import User

class UpdateProfile(FlaskForm):
  bio = TextAreaField('Tell us more about yourself', validators=[Required()])
  submit = SubmitField('Submit')

class PitchForm(FlaskForm):
  pitch_title = StringField('Pitch TItle', validators=[Required()])
  content = TextAreaField('Enter Pitch details', validators=[Required()])
  category = SelectField('Select Pitch Category', choices=[('Product Pitch', 'Product Pitch'),
  ('Interview Pitch', 'Interview Pitch'),('Idea Pitch','Idea Pitch')], validators = [Required()])
  submit = SubmitField('Pitch')

class CommentForm(FlaskForm):
  comment = TextAreaField('Leave a comment', validators=[Required()])
  submit = SubmitField('Comment')