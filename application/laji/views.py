from flask import render_template
from flask_login import login_required, current_user

from application import app
from application.laji.models import Laji


@app.route("/laji")
@login_required
def laji_index():
    return render_template("laji/list.html", lajit=Laji.find_maarat_lajeittain_by_user_id(current_user.id))
