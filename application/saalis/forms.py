from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class SaalisForm(FlaskForm):
    laji = StringField("Laji", [validators.Length(min=2)])
    paikka = StringField("Paikka")
    maara = IntegerField("Määrä")
    koordinaatit = StringField("Koordinaatit")

 
    class Meta:
        csrf = False