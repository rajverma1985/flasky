from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Creating a form object from Flask form class

class NewForm(FlaskForm):
    name = StringField('What is your Name', validators=[DataRequired()])
    submit = SubmitField('Submit Form')
