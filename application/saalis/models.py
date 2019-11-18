from application import db

from sqlalchemy.sql import text


class Saalis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    laji = db.Column(db.String(100), nullable=False)
    paikka = db.Column(db.String(100), nullable=False)
    paivamaara = db.Column(db.DateTime, default=db.func.current_timestamp())
    maara = db.Column(db.Integer, nullable=False)
    koordinaatit = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    def __init__(self, laji, paikka, maara, koordinaatit):
        self.laji = laji
        self.paikka = paikka
        self.maara = maara
        self.koordinaatit = koordinaatit
    
    @staticmethod
    def find_users_saaliit(user_id):
        stmt = text("SELECT * FROM Saalis WHERE account_id = :id").params(id=user_id)
        res = db.engine.execute(stmt)

        return res
