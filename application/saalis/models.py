from sqlalchemy.sql import text

from application import db


class Saalis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paivamaara = db.Column(db.DateTime, default=db.func.current_timestamp())
    maara = db.Column(db.Integer, nullable=False)
    koordinaatit = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)
    sijainti_id = db.Column(db.Integer, db.ForeignKey(
        'sijainti.id'), nullable=False)
    laji_id = db.Column(db.Integer, db.ForeignKey(
        'laji.id'), nullable=False)

    def __init__(self, maara, koordinaatit):
        self.maara = maara
        self.koordinaatit = koordinaatit

    @staticmethod
    def find_users_saaliit(user_id):
        stmt = text(
            "SELECT Account.name, Saalis.id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi "
            "FROM Saalis "
            "JOIN Account ON Saalis.account_id = account.id "
            "JOIN Sijainti ON Saalis.sijainti_id = sijainti.id "
            "JOIN Laji ON Saalis.laji_id = laji.id "
            "WHERE Account.id = :id").params(id=user_id)
        res = db.engine.execute(stmt)

        return res


class Sijainti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alue = db.Column(db.String(20), nullable=False)

    def __init__(self, alue):
        self.alue = alue

    @staticmethod
    def find_alue_id(alueenNimi):
        stmt = text("SELECT id FROM Sijainti WHERE Sijainti.alue = :alue").params(alue=alueenNimi)

        res = db.engine.execute(stmt).first()

        if not res:
            sijainti = Sijainti(alueenNimi)
            db.session().add(sijainti)
            db.session().commit()
            return sijainti.id

        return res.id


class Laji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(20), nullable=False)

    def __init__(self, nimi):
        self.nimi = nimi

    @staticmethod
    def find_laji_id(lajinNimi):
        stmt = text("SELECT id FROM Laji WHERE Laji.nimi = :nimi").params(nimi=lajinNimi)

        res = db.engine.execute(stmt).first()

        if not res:
            laji = Laji(lajinNimi)
            db.session().add(laji)
            db.session().commit()
            return laji.id

        return res.id
