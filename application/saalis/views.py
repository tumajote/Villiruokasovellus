from application import app, db
from flask import render_template, request, redirect, url_for
from application.saalis.models import Saalis
from application.saalis.forms import SaalisForm


@app.route("/saalis", methods=["GET"])
def saalis_index():
    return render_template("saalis/list.html", saaliit=Saalis.query.all())


@app.route("/saalis/new/")
def saalis_form():
    return render_template("saalis/new.html", form=SaalisForm())


@app.route("/saalis/", methods=["POST"])
def saalis_create():
    form = SaalisForm(request.form)

    if not form.validate():
        return render_template("saalis/new.html", form = form)

    laji = form.laji.data
    paikka = form.paikka.data
    maara = form.maara.data
    koordinaatit = form.koordinaatit.data
    t = Saalis(laji, paikka, maara, koordinaatit)
    db.session().add(t)
    db.session().commit()
    return redirect(url_for("saalis_index"))
