from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_manager
from application import app, db
from application.laji.models import Laji
from application.saalis.forms import SearchSaalisForm, CreateSaalisForm
from application.saalis.models import Saalis
from application.sijainti.models import Sijainti



@app.route("/sijainti")
@login_required
def sijainti_index():
    return render_template("sijainti/list.html", sijainnit=Sijainti.find_maarat_alueittain_by_user_id(current_user.id))
