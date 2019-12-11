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


@app.route("/saalis/")
@login_required
def saalis_index():
    return render_template("saalis/list.html", saaliit=Saalis.find_users_saaliit(current_user.id),
                           form=SearchSaalisForm())


@app.route("/saalis/search", methods=["GET"])
@login_required
def saalis_search():
    form = SearchSaalisForm()
    search = request.args.get("kenen")
    maara = Saalis.sum_of_all_maara(current_user.id).first()
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

    return render_template("saalis/list.html", saaliit=saaliit, maara=maara,
                           form=form)


@app.route("/saalis/new/")
@login_required
def saalis_form():
    return render_template("saalis/new.html", form=CreateSaalisForm())


@app.route("/saalis/new", methods=["POST"])
@login_required
def saalis_create():
    form = CreateSaalisForm(request.form)

    if not form.validate():
        return render_template("saalis/new.html", form=form)

    maara = form.maara.data
    koordinaatit = form.koordinaatit.data
    saalis = Saalis(maara, koordinaatit)

    saalis.account_id = current_user.id
    sijaintipk = Sijainti.find_alue_id(form.alue.data)
    saalis.sijainti_id = sijaintipk
    lajipk = Laji.find_laji_id(form.laji.data)
    saalis.laji_id = lajipk
    saalis.julkinen = form.julkinen.data

    db.session().add(saalis)
    db.session().commit()
    return redirect(url_for("saalis_search"))


@app.route("/saalis/<saalis_id>", methods=["GET"])
@login_required
def saalis_edit_form(saalis_id):
    saalis = Saalis.query.get(saalis_id)

    if saalis.account_id != current_user.id:
        return login_manager.user_unauthorized()

    sijainti = Sijainti.query.get(saalis.sijainti_id)
    laji = Laji.query.get(saalis.laji_id)

    form = CreateSaalisForm(request.form)

    form.laji.data = laji.nimi
    form.alue.data = sijainti.alue
    form.maara.data = saalis.maara
    form.koordinaatit.data = saalis.koordinaatit
    form.julkinen.data = saalis.julkinen

    return render_template("saalis/edit.html", saalis=saalis, form=form, sijainti=sijainti, laji=laji)


@app.route("/saalis/<saalis_id>/", methods=["POST"])
@login_required
def saalis_edit(saalis_id):
    saalis = Saalis.query.get(saalis_id)

    if saalis.account_id != current_user.id:
        return login_manager.user_unauthorized()

    sijainti = Sijainti.query.get(saalis.sijainti_id)
    laji = Laji.query.get(saalis.laji_id)
    form = CreateSaalisForm(request.form)

    if form.poista.data:
        db.session().delete(saalis)
        db.session().commit()
        return redirect(url_for("saalis_search"))

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

    if saalis.julkinen != form.julkinen.data:
        saalis.julkinen = form.julkinen.data
        muutos = True

    if muutos:
        db.session().commit()
    return redirect(url_for("saalis_search"))
