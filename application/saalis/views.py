from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_manager

from application import app, db
from application.auth.models import User
from application.laji.models import Laji
from application.saalis.forms import SearchSaalisForm, CreateSaalisForm, ShareForm
from application.saalis.models import Saalis, Jaot
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
    elif search == "jaetut":
        saaliit = Jaot.get_shared_to_user(current_user.id)
        return render_template("saalis/list_shared.html", saaliit=saaliit, form=form)
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
        form = CreateSaalisForm(request.form)
        if form.poista.data:
            db.session().delete(saalis)
            db.session().commit()
            return redirect(url_for("saalis_search"))

        if form.validate():
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


@app.route("/saalis/share/<saalis_id>", methods=["GET", "POST"])
@login_required
def share(saalis_id):
    form = ShareForm(request.form)
    shares = Jaot.get_users_shares(saalis_id)
    saalis = Saalis.find_saalis(saalis_id, current_user.id)

    if request.method == 'POST':
        if form.validate():

            user = User.query.filter_by(username=form.username.data).first()

            if user == current_user:
                return render_template("saalis/share.html", form=form, saalis=saalis, shares=shares,
                                       error="Et voi jakaa itsesi kanssa!")

            if not user:
                return render_template("saalis/share.html", form=form, saalis=saalis, shares=shares,
                                       error="Käyttäjänimeä ei ole olemassa!")

            if Jaot.query.filter_by(kohde_account_id=user.id,
                                    jaettu_saalis_id=saalis_id).first():
                return render_template("saalis/share.html", form=form, saalis=saalis, shares=shares,
                                       error="Olet jo jakanut saaliin kyseisen käyttäjän kanssa!")

            shared = Jaot(current_user.id, user.id, saalis_id)
            db.session().add(shared)
            db.session().commit()
            return redirect(url_for("share", saalis_id=saalis.id))

    return render_template("saalis/share.html", form=form, saalis=saalis, shares=shares)


@app.route("/saalis/share/delete/<user_id>/<saalis_id>", methods=["POST"])
@login_required
def remove_share(user_id, saalis_id):
    Jaot.delete_share(user_id, saalis_id)
    return render_template("saalis/share.html", form=ShareForm(request.form), saalis=Saalis.query.get(saalis_id),
                           shares=Jaot.get_users_shares(saalis_id))
