from flask import render_template
from flask_login import login_required, current_user

from application import app
from application.sijainti.models import Sijainti


@app.route("/sijainti")
@login_required
def sijainti_index():
    return render_template("sijainti/list.html", sijainnit=Sijainti.find_maarat_alueittain_by_user_id(current_user.id))
