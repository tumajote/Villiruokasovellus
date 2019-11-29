from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, RadioField, validators


class CreateSaalisForm(FlaskForm):
    maara = IntegerField("Määrä", [validators.InputRequired()])
    koordinaatit = StringField("Koordinaatit", [validators.Length(min=20)])

    laji = StringField("Laji", [validators.Length(min=2)])
    alue = StringField("Alue", [validators.Length(min=2)])

    julkinen = BooleanField("Julkinen")
    poista = BooleanField("Poista")

    class Meta:
        csrf = False


class SearchSaalisForm(FlaskForm):
    kenen = RadioField("kenen", choices=[("omat", "Omat saaliit"), ("julkiset", "Julkiset saaliit"),
                                         ("julkisetJaOmat", "Julkiset ja omat saaliit")], default="omat")

    alueittain = BooleanField("Alueittain")
    lajeittain = BooleanField("Lajeittain")
    isoinMaaraEnsin = BooleanField("Alueittain")

    class Meta:
        csrf = False
