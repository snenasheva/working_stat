from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, Length, Optional, ValidationError


class RegistrationForm(FlaskForm):
    def validate_username(self):
        pass

    def validate_email(self):
        pass

    username = StringField(label='username', validators=[Length(min=5, max=70), DataRequired()])
    password1 = PasswordField(label='password', validators=[Length(min=8, max=30), DataRequired()])
    password2 = PasswordField(label='confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create account')


class LoginForm(FlaskForm):
    username = StringField(label='insert your username', validators=[DataRequired()])
    password = PasswordField(label='insert your password', validators=[DataRequired()])
    submit = SubmitField(label='Log In')
