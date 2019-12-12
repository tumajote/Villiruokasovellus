from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, RadioField, validators


class CreateSaalisForm(FlaskForm):
    maara = IntegerField("Määrä", [validators.data_required(message="Kenttä ei voi olla tyhjä"),
                                   validators.number_range(min=1, max=1000000,
                                                           message="Määrän on oltava luku väliltä 1-1000000")])

    koordinaatit = StringField("Koordinaatit", [validators.data_required(message="Kenttä ei voi olla tyhjä"),
                                                validators.regexp(
                                                    "\-?(90|[0-8]?[0-9]\.[0-9]{0,6})\, \-?(180|(1[0-7][0-9]|[0-9]{0,2})\.[0-9]{0,6})",
                                                    message="Anna koordinaatit desimaaliasteina (Decimal Degrees, DD) "
                                                            + "(dd.dddddd, dd.dddddd). Voit kopioida koordinaatit suoraan Google Mapsista")])

    laji = StringField("Laji", [validators.data_required(message="Kenttä ei voi olla tyhjä"),
                                validators.Length(min=3, max=20,
                                                  message="Lajin nimen on oltava pituudeltaan 3-20 merkkiä")])

    alue = StringField("Alue", [validators.data_required(message="Kenttä ei voi olla tyhjä"),
                                validators.Length(min=3, max=20,
                                                  message="Lajin nimen on oltava pituudeltaan 3-20 merkkiä")])

    julkinen = BooleanField("Julkinen")
    poista = BooleanField("Poista")

    class Meta:
        csrf = False


class SearchSaalisForm(FlaskForm):
    kenen = RadioField("kenen", choices=[("omat", "Omat saaliit"), ("julkiset", "Julkiset saaliit"),
                                         ("julkisetJaOmat", "Julkiset ja omat saaliit"), ("jaetut", "Sinulle jaetut")],
                       default="omat")

    class Meta:
        csrf = False


class ShareForm(FlaskForm):
    username = StringField("Käyttäjänimi", [validators.data_required(message='Kenttä ei voi olla tyhjä'),
                                            validators.Length(min=3, max=10,
                                                              message="Käyttäjänimen on oltava pituudeltaan 3-10 merkkiä pitkä")])

    class Meta:
        csrf = False
