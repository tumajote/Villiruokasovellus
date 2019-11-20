from sqlalchemy.sql import text

from application import db


class Saalis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    laji = db.Column(db.String(100), nullable=False)
    paivamaara = db.Column(db.DateTime, default=db.func.current_timestamp())
    maara = db.Column(db.Integer, nullable=False)
    koordinaatit = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)
    sijainti_id = db.Column(db.Integer, db.ForeignKey(
        'sijainti.id'), nullable=False)

    def __init__(self, laji, maara, koordinaatit):
        self.laji = laji
        self.maara = maara
        self.koordinaatit = koordinaatit

    @staticmethod
    def find_users_saaliit(user_id):
        stmt = text("SELECT * FROM Saalis,Sijainti WHERE account_id = :id").params(id=user_id)
        res = db.engine.execute(stmt)

        return res


class Sijainti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alue = db.Column(db.String(20), nullable=False)

    def __init__(self, alue):
        self.alue = alue


    @staticmethod
    def find_alue(alueenNimi):
        stmt = text("SELECT id FROM Sijainti WHERE alue = :alue").params(alue=alueenNimi)

        res = db.engine.execute(stmt).first()

        if not res:
            return 0

        return res.id
