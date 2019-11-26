from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.forms import LoginForm, SignInForm
from application.auth.models import User


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form,
                               error="Käyttäjänimi tai salasana on väärin!")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/signin", methods=["GET", "POST"])
def auth_signin():
    if request.method == "GET":
        return render_template("auth/signinform.html", form=SignInForm())

    form = SignInForm(request.form)
    # mahdolliset validoinnit

    if not form.validate():
        return render_template("auth/signinform.html", form=form)

    if not form.password.data == form.confirmPassword.data:
        return render_template("auth/signinform.html", form=form,
                               error="Salasana ja salasananvarmistus eivät täsmää!")

    if User.query.filter_by(username=form.username.data).first():
        return render_template("auth/signinform.html", form=form,
                               error="Käyttäjänimi on jo käytössä!")

    user = User(form.username.data, form.username.data, form.password.data)
    db.session().add(user)
    db.session().commit()
    login_user(user)
    return redirect(url_for("index"))
