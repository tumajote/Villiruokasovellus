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
