from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class JobPostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    skills = TextAreaField('Skills Required', validators=[DataRequired()])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    category = RadioField(u'Select job category',  choices=[('Programming & Development', 'Programming & Development'), ('Design & Art', 'Design & Art'), ('Writing & Translation', 'Writing & Translation'), ('Sales & Marketing', 'Sales & Marketing'), ('Administrative & Secretarial', 'Administrative & Secretarial'), ('Education & Training', 'Education & Training'), ('Business & Finance', 'Business & Finance'), ('Engineering & Architecture', 'Engineering & Architecture'), ('Legal', 'Legal'), ('Others', 'Others')], validators=[DataRequired()])
    min_budget = StringField('Budget (in $)', validators=[DataRequired()])
    create = SubmitField('Create Job Post')
    update = SubmitField('Update Job Post')
