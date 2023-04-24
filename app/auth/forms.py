from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 30)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         'Usernames must have only '
                                                                                         'letter, numbers or dots or '
                                                                                         'underscore')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match'),
                                                     Length(8, 30)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register Now')
