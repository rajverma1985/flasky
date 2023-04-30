from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from ..models import User


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

    def email_validation(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError("Email is already registered!")

    def user_validation(self, user_field):
        if User.query.filter_by(email=user_field.data).first():
            raise ValidationError("Username is already in user")

