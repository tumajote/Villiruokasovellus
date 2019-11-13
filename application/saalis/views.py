from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application.saalis.models import Saalis
from application.saalis.forms import SaalisForm


@app.route("/saalis")
def saalis_index():
    return render_template("saalis/list.html", saaliit=Saalis.query.all())


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

    laji = form.laji.data
    paikka = form.paikka.data
    maara = form.maara.data
    koordinaatit = form.koordinaatit.data
    t = Saalis(laji, paikka, maara, koordinaatit)
    t.account_id = current_user.id
    db.session().add(t)
    db.session().commit()
    return redirect(url_for("saalis_index"))


@app.route("/saalis/<saalis_id>/", methods=["GET", "POST"])
@login_required
def saalis_editForm(saalis_id):
    saalis = Saalis.query.get(saalis_id)

    form = SaalisForm(request.form)

    if request.method == 'POST':

        if form.poista:
            db.session().delete(saalis)
            db.session().commit()
            return redirect(url_for("saalis_index"))

        muutos = False
        if saalis.laji != form.laji.data:
            saalis.laji = form.laji.data
            muutos = True

        if saalis.paikka != form.paikka.data:
            saalis.paikka = form.paikka.data
            muutos = True

        if saalis.maara != form.maara.data:
            saalis.maara = form.maara.data
            muutos = True

        if saalis.koordinaatit != form.koordinaatit.data:
            saalis.koordinaatit = form.koordinaatit.data
            muutos = True

        if not form.validate():
            return render_template("saalis/edit.html", saalis=saalis, form=form)

        if muutos:
            db.session().commit()

    form.laji.data = saalis.laji
    form.paikka.data = saalis.paikka
    form.maara.data = saalis.maara
    form.koordinaatit.data = saalis.koordinaatit

    return render_template("saalis/edit.html", saalis=saalis, form=form)
