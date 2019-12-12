from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from application import app, db
from application.auth.forms import LoginForm, SignInForm, EditNameForm, EditPassWordForm
from application.auth.models import User
from application.saalis.models import Saalis


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(
                username=form.username.data, password=form.password.data).first()
            if not user:
                return render_template("auth/login_form.html", form=form,
                                       error="Käyttäjänimi tai salasana on väärin!")
            login_user(user)
            return redirect(url_for("index"))
    return render_template("auth/login_form.html", form=form)


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/signin", methods=["GET", "POST"])
def auth_signin():
    form = SignInForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first():
                return render_template("auth/signin_form.html", form=form,
                                       error="Käyttäjänimi on jo käytössä!")
            user = User(form.username.data, form.password.data)
            db.session().add(user)
            db.session().commit()
            login_user(user)
            return redirect(url_for("index"))
    return render_template("auth/signin_form.html", form=form)


@app.route("/auth/user_profile", methods=["GET"])
@login_required
def user_profile_index():
    return render_template("auth/user_profile.html", user=current_user)


@app.route("/auth/edit_username", methods=["GET", "POST"])
@login_required
def edit_username():
    form = EditNameForm(request.form)
    if request.method == 'POST':
        if User.query.filter_by(username=form.username.data).first():
            return render_template("auth/edit_username.html", form=form,
                                   error="Käyttäjänimi on jo käytössä!")
        if form.validate_on_submit():
            user = current_user
            user.username = form.username.data
            db.session().commit()
            return redirect(url_for("user_profile_index"))
    return render_template("auth/edit_username.html", form=form)


@app.route("/auth/edit_password", methods=["GET", "POST"])
@login_required
def edit_password():
    form = EditPassWordForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = form.newpassword.data
            db.session.commit()
            return redirect(url_for("user_profile_index"))
    return render_template("auth/edit_password.html", form=form)


@app.route("/auth/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(password=form.password.data).first()

        if not user == current_user:
            return render_template("auth/delete.html", form=form, error="Salasana on väärin!")

        Saalis.delete_users_saaliit(current_user.id)
        db.session().delete(user)
        db.session.commit()
        return redirect(url_for("user_profile_index"))

    return render_template("auth/delete.html", form=form)
