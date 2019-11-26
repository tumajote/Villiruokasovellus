from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.saalis.forms import SaalisForm
from application.saalis.models import Saalis, Sijainti, Laji


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
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    if not form.validate():
        return render_template("saalis/new.html", form=form)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    maara = form.maara.data
    koordinaatit = form.koordinaatit.data
    saalis = Saalis(maara, koordinaatit)

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    saalis.account_id = current_user.id
    sijaintipk = Sijainti.find_alue_id(form.alue.data)
    saalis.sijainti_id = sijaintipk
    lajipk = Laji.find_laji_id(form.laji.data)
    saalis.laji_id = lajipk

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    db.session().add(saalis)
    db.session().commit()
    return redirect(url_for("saalis_index"))


@app.route("/saalis/<saalis_id>/", methods=["GET"])
@login_required
def saalis_edit_form(saalis_id):
    saalis = Saalis.query.get(saalis_id)
    sijainti = Sijainti.query.get(saalis.sijainti_id)
    laji = Laji.query.get(saalis.laji_id)

    form = SaalisForm(request.form)

    form.laji.data = laji.nimi
    form.alue.data = sijainti.alue
    form.maara.data = saalis.maara
    form.koordinaatit.data = saalis.koordinaatit

    return render_template("saalis/edit.html", saalis=saalis, form=form, sijainti=sijainti, laji=lajiq)


@app.route("/saalis/<saalis_id>/", methods=["POST"])
@login_required
def saalis_edit(saalis_id):
    saalis = Saalis.query.get(saalis_id)
    sijainti = Sijainti.query.get(saalis.sijainti_id)
    laji = Laji.query.get(saalis.laji_id)
    form = SaalisForm(request.form)

    if form.poista.data:
        db.session().delete(saalis)
        db.session().commit()
        return redirect(url_for("saalis_index"))

    if not form.validate():
        return render_template("saalis/edit.html", saalis=saalis, form=form, laji=laji)

    muutos = False
    if laji.nimi != form.laji.data:
        saalis.laji_id = Laji.find_laji_id(form.laji.data)
        laji = Laji.query.get(saalis.laji_id)
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
    return render_template("saalis/edit.html", saalis=saalis, form=form, sijainti=sijainti, laji=laji)
