from flask import render_template
from flask_login import current_user,user_logged_in

from application import app
from application.saalis.models import Saalis


@app.route("/")
def index():
    if current_user.is_authenticated:
        maara = Saalis.sum_of_all_maara(current_user.id)
        return render_template("index.html", maara=maara)
    return render_template("index.html")
