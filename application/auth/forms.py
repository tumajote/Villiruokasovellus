from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class SignInForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3, max=10)])
    password = PasswordField("Password", [validators.Length(min=6)])
    confirmPassword = PasswordField("Confirm password")

    class Meta:
        csrf = False