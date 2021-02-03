from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    skills = TextAreaField('Skills', validators=[DataRequired()])
    min_starting_rate = TextAreaField('Minimum Starting Rate', validators=[DataRequired()])
    max_starting_rate = TextAreaField('Maximum Starting Rate', validators=[DataRequired()])
    min_hourly_rate = TextAreaField('Minimum Hourly Rate', validators=[DataRequired()])
    max_hourly_rate = TextAreaField('Maximum Hourly Rate', validators=[DataRequired()])
    create = SubmitField('Create Freelancer Profile')
    update = SubmitField('Update Freelancer Profile')
