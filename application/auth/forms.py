from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators,BooleanField


class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi")
    password = PasswordField("Salasana")


    class Meta:
        csrf = False


class SignInForm(FlaskForm):
    username = StringField("Käyttäjänimi", [validators.Length(min=3, max=10)])
    password = PasswordField("Salasana", [validators.Length(min=6)])
    confirmPassword = PasswordField("Varmista salasana")
    class Meta:
        csrf = False

class EditNameForm(FlaskForm):
    username = StringField("Uusi käyttäjänimi", [validators.Length(min=3, max=10)])
    class Meta:
        csrf = False

class EditPassWordForm(FlaskForm):
    newpassword = PasswordField("Uusi salasana", [validators.Length(min=6)])
    confirmPassword = PasswordField("Varmista salasana")
    class Meta:
        csrf = False