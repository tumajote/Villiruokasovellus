from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, validators


class SaalisForm(FlaskForm):
    maara = IntegerField("Määrä", [validators.InputRequired()])
    koordinaatit = StringField("Koordinaatit", [validators.Length(min=20)])

    laji = StringField("Laji", [validators.Length(min=2)])
    alue = StringField("Alue", [validators.Length(min=2)])

    julkinen = BooleanField("Julkinen")
    poista = BooleanField("Poista")

    class Meta:
        csrf = False
