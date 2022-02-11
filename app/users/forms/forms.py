"""
The module for user RegistrationForm.
Amer Ahmed
Amir Ramic
Supervisor: Joakim Wassberg
Version 0.0.1
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms import BooleanField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from wtforms.validators import EqualTo, ValidationError
from app.models.models.models import User


class RegistrationForm(FlaskForm):
    """User registrationForm"""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=64)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):  # Verify username
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one!')

    def validate_email(self, email):  # Verify email
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one!')


class LoginForm(FlaskForm):
    """User LoginForm"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class UpdateAccountForm(FlaskForm):
    """User Updated Account"""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):  # Verify username
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one!')

    def validate_email(self, email):  # Verify email
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one!')


class RequestResetForm(FlaskForm):
    """User Request Reset Password"""
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):  # Verify email
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no  account with with email. Please signup first!')


class ResetPasswordForm(FlaskForm):
    """User Confirm Reset Password"""
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=64)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class SearchForm(FlaskForm):
    """User search form posts"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Search')
