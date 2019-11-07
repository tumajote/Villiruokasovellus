from application import app,db
from flask import render_template, request, redirect, url_for
from application.saalis.models import Saalis

@app.route("/saalis", methods=["GET"])
def saalis_index():
    return render_template("saalis/list.html", saaliit = Saalis.query.all())



@app.route("/saalis/new/")
def saalis_form():
    return render_template("saalis/new.html")

@app.route("/saalis/", methods=["POST"])
def saalis_create():
    laji = request.form.get("laji")
    paikka = request.form.get("paikka")
    maara = request.form.get("maara")
    koordinaatit = request.form.get("koordinaatit")
    t = Saalis(laji,paikka,maara,koordinaatit)
    db.session().add(t)
    db.session().commit()
    return redirect(url_for("saalis_index"))