from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.saalis.forms import SaalisForm
from application.saalis.models import Saalis, Sijainti


@app.route("/saalis")
@login_required
def saalis_index():
    return render_template("saalis/list.html", saaliit=Saalis.find_users_saaliit(current_user.id))


@app.route("/saalis/new/")
@login_required
def saalis_form():
    return render_template("saalis/new.html", form=SaalisForm())


@app.route("/saalis/new", methods=["POST"])
@login_required
def saalis_create():
    form = SaalisForm(request.form)

    if not form.validate():
        return render_template("saalis/new.html", form=form)

    alue = form.alue.data
    sijaintipk = Sijainti.find_alue_id(alue)

    laji = form.laji.data
    maara = form.maara.data
    koordinaatit = form.koordinaatit.data
    saalis = Saalis(laji, maara, koordinaatit)
    saalis.account_id = current_user.id
    saalis.sijainti_id = sijaintipk

    db.session().add(saalis)
    db.session().commit()
    return redirect(url_for("saalis_index"))


@app.route("/saalis/<saalis_id>/", methods=["GET"])
@login_required
def saalis_edit_form(saalis_id):
    saalis = Saalis.query.get(saalis_id)
    sijainti = Sijainti.query.get(saalis.sijainti_id)
    form = SaalisForm(request.form)

    form.laji.data = saalis.laji
    form.alue.data = sijainti.alue
    form.maara.data = saalis.maara
    form.koordinaatit.data = saalis.koordinaatit

    return render_template("saalis/edit.html", saalis=saalis, form=form, sijainti=sijainti)


@app.route("/saalis/<saalis_id>/", methods=["POST"])
@login_required
def saalis_edit(saalis_id):
    saalis = Saalis.query.get(saalis_id)
    sijainti = Sijainti.query.get(saalis.sijainti_id)
    form = SaalisForm(request.form)

    if form.poista.data:
        db.session().delete(saalis)
        db.session().commit()
        return redirect(url_for("saalis_index"))

    if not form.validate():
        return render_template("saalis/edit.html", saalis=saalis, form=form)

    muutos = False
    if saalis.laji != form.laji.data:
        saalis.laji = form.laji.data
        muutos = True

    if sijainti.alue != form.alue.data:
        saalis.sijainti_id = Sijainti.find_alue_id(form.alue.data)
        sijainti = Sijainti.query.get(saalis.sijainti_id)
        muutos = True

    if saalis.maara != form.maara.data:
        saalis.maara = form.maara.data
        muutos = True

    if saalis.koordinaatit != form.koordinaatit.data:
        saalis.koordinaatit = form.koordinaatit.data
        muutos = True

    if muutos:
        db.session().commit()
    return render_template("saalis/edit.html", saalis=saalis, form=form, sijainti=sijainti)
