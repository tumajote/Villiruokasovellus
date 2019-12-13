from flask import render_template
from flask_login import current_user

from application import app
from application.saalis.models import Saalis


@app.route("/")
def index():
    if current_user.is_authenticated:
        maara = Saalis.sum_of_all_maara(current_user.id)
        if not maara:
            maara = 0
        return render_template("index.html", maara=maara)
    return render_template("index.html")
