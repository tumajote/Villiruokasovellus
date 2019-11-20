from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,BooleanField,FloatField, validators

class SaalisForm(FlaskForm):

    maara = IntegerField("Määrä")
    koordinaatit = StringField("Koordinaatit")

    laji = StringField("Laji", [validators.Length(min=2)])
    alue = StringField("Alue")
    poista = BooleanField("Poista")


 
    class Meta:
        csrf = False
        