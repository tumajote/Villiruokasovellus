from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi")
    password = PasswordField("Salasana")

    class Meta:
        csrf = False


class SignInForm(FlaskForm):
    username = StringField("Käyttäjänimi", [validators.data_required(message='Kenttä ei voi olla tyhjä'),
                                            validators.Length(min=3, max=10,
                                                              message="Käyttäjänimen on oltava pituudeltaan 3-10 merkkiä pitkä")])
    password = PasswordField("Salasana", [validators.data_required(message='Kenttä ei voi olla tyhjä'),
                                          validators.equal_to('confirmPassword', message='Salasanat eivät täsmää'),
                                          validators.Length(min=6, max=20,
                                                            message="Salasanan on oltava pituudeltaan 6-20 merkkiä pitkä")])
    confirmPassword = PasswordField("Varmista salasana")

    class Meta:
        csrf = False


class EditNameForm(FlaskForm):
    username = StringField("Uusi käyttäjänimi", [validators.data_required(message='Kenttä ei voi olla tyhjä'),
                                                 validators.Length(min=3, max=10,
                                                                   message="Käyttäjänimen on oltava pituudeltaan 3-10 merkkiä pitkä")])

    class Meta:
        csrf = False


class EditPassWordForm(FlaskForm):
    newpassword = PasswordField("Uusi salasana", [validators.data_required(message='Kenttä ei voi olla tyhjä'),
                                                  validators.equal_to('confirmPassword',
                                                                      message='Salasanat eivät täsmää'),
                                                  validators.Length(min=6, max=20,
                                                                    message="Salasanan on oltava pituudeltaan 6-20 merkkiä pitkä")])
    confirmPassword = PasswordField("Varmista salasana")

    class Meta:
        csrf = False
