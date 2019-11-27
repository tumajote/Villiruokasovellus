from flask import render_template
from application import app
from application.saalis.models import Saalis

@app.route("/")
def index():
    return render_template("saalis/julkinen.html", saaliit=Saalis.find_all_public_saaliit())