from sqlalchemy.sql import text

from application import db


class Saalis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paivamaara = db.Column(db.Date, default=db.func.current_date())
    maara = db.Column(db.Integer, nullable=False)
    koordinaatit = db.Column(db.String(100), nullable=False)
    julkinen = db.Column(db.Boolean, nullable=False)
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
            "SELECT Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi, Saalis.julkinen "
            "FROM Saalis "
            "JOIN Account ON Saalis.account_id = account.id "
            "JOIN Sijainti ON Saalis.sijainti_id = sijainti.id "
            "JOIN Laji ON Saalis.laji_id = laji.id "
            "WHERE Account.id = :id").params(id=user_id)
        res = db.engine.execute(stmt)

        return res

    @staticmethod
    def find_all_public_saaliit():
        stmt = text(
            "SELECT Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Saalis.julkinen, Sijainti.alue, Laji.nimi, Saalis.julkinen "
            "FROM Saalis "
            "JOIN Account ON Saalis.account_id = account.id "
            "JOIN Sijainti ON Saalis.sijainti_id = sijainti.id "
            "JOIN Laji ON Saalis.laji_id = laji.id "
            "WHERE Saalis.julkinen = TRUE ")
        res = db.engine.execute(stmt)

        return res

    @staticmethod
    def find_users_and_public_saaliit(user_id):
        stmt = text(
            "SELECT Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi, Saalis.julkinen "
            "FROM Saalis "
            "JOIN Account ON Saalis.account_id = account.id "
            "JOIN Sijainti ON Saalis.sijainti_id = sijainti.id "
            "JOIN Laji ON Saalis.laji_id = laji.id "
            "WHERE Account.id = :id "
            "OR Saalis.julkinen = TRUE ").params(id=user_id)
        res = db.engine.execute(stmt)

        return res

    @staticmethod
    def sum_of_all_maara(user_id):
        stmt = text(
            "SELECT SUM(saalis.maara) as summa "
            "FROM Saalis "
            "JOIN Account ON Saalis.account_id = account.id "
            "WHERE Account.id = :id ").params(id=user_id)
        res = db.engine.execute(stmt)
        res = res.first()
        res = res[0]
        return res

    @staticmethod
    def delete_users_saaliit(user_id):
        stmt = text(
            "DELETE FROM Saalis "
            "WHERE account_id = :id ").params(id=user_id)
        res = db.engine.execute(stmt)
