from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_manager
from application import app, db
from application.laji.models import Laji
from application.saalis.forms import SearchSaalisForm, CreateSaalisForm
from application.saalis.models import Saalis
from application.sijainti.models import Sijainti



@app.route("/laji")
@login_required
def laji_index():
    return render_template("laji/list.html", lajit=Laji.find_maarat_lajeittain_by_user_id(current_user.id))
