from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_manager

from application import app, db
from application.laji.models import Laji
from application.saalis.forms import SearchSaalisForm, CreateSaalisForm
from application.saalis.models import Saalis
from application.sijainti.models import Sijainti


@app.route("/saalis/public")
def saalis_public_index():
    return render_template("saalis/public.html", saaliit=Saalis.find_all_public_saaliit())


@app.route("/saalis/search", methods=["GET"])
@login_required
def saalis_search():
    form = SearchSaalisForm()
    search = request.args.get("kenen")

    if not search:
        form.kenen.data = "omat"
        search = "omat"
    else:
        form.kenen.data = search

    if search == "omat":
        saaliit = Saalis.find_users_saaliit(current_user.id)
    elif search == "julkiset":
        saaliit = Saalis.find_all_public_saaliit()
    elif search == "julkisetJaOmat":
        saaliit = Saalis.find_users_and_public_saaliit(current_user.id)

    return render_template("saalis/list.html", saaliit=saaliit, form=form)


@app.route("/saalis/new", methods=["GET", "POST"])
@login_required
def saalis_create():
    form = CreateSaalisForm(request.form)
    if request.method == 'POST':
        if form.validate():
            maara = form.maara.data
            koordinaatit = form.koordinaatit.data
            saalis = Saalis(maara, koordinaatit)

            saalis.account_id = current_user.id
            sijaintipk = Sijainti.find_alue_id_or_create_missing_alue(form.alue.data)
            saalis.sijainti_id = sijaintipk
            lajipk = Laji.find_laji_id_or_create_missing_laji(form.laji.data)
            saalis.laji_id = lajipk
            saalis.julkinen = form.julkinen.data

            db.session().add(saalis)
            db.session().commit()
            return redirect(url_for("saalis_search"))

    return render_template("saalis/new.html", form=form)


@app.route("/saalis/<saalis_id>", methods=["GET", "POST"])
@login_required
def saalis_edit(saalis_id):
    saalis = Saalis.query.get(saalis_id)
    sijainti = Sijainti.query.get(saalis.sijainti_id)
    laji = Laji.query.get(saalis.laji_id)

    if saalis.account_id != current_user.id:
        return login_manager.user_unauthorized()

    form = CreateSaalisForm(request.form)

    form.laji.data = laji.nimi
    form.alue.data = sijainti.alue
    form.maara.data = saalis.maara
    form.koordinaatit.data = saalis.koordinaatit
    form.julkinen.data = saalis.julkinen

    if request.method == 'POST':
        if form.validate():

            if form.poista.data:
                db.session().delete(saalis)
                db.session().commit()
                return redirect(url_for("saalis_search"))

            muutos = False
            if laji.nimi != form.laji.data:
                saalis.laji_id = Laji.find_laji_id_or_create_missing_laji(form.laji.data)
                laji = Laji.query.get(saalis.laji_id)
                muutos = True

            if sijainti.alue != form.alue.data:
                saalis.sijainti_id = Sijainti.find_alue_id_or_create_missing_alue(form.alue.data)
                sijainti = Sijainti.query.get(saalis.sijainti_id)
                muutos = True

            if saalis.maara != form.maara.data:
                saalis.maara = form.maara.data
                muutos = True

            if saalis.koordinaatit != form.koordinaatit.data:
                saalis.koordinaatit = form.koordinaatit.data
                muutos = True

            if saalis.julkinen != form.julkinen.data:
                saalis.julkinen = form.julkinen.data
                muutos = True

            if muutos:
                db.session().commit()
            return render_template("saalis/edit.html", saalis=saalis, form=form, laji=laji, sijainti=sijainti)

    return render_template("saalis/edit.html", saalis=saalis, form=form, sijainti=sijainti, laji=laji)
