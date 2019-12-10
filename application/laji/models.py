from sqlalchemy.sql import text

from application import db


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

    @staticmethod
    def find_maarat_lajeittain_by_user_id(userId):
        stmt = text(
            "SELECT Laji.nimi, SUM(Saalis.maara) AS maara "
            "FROM Laji "
            "LEFT JOIN Saalis ON Laji.id = Saalis.laji_id "
            "JOIN Account ON Saalis.account_id = account.id "
            "WHERE Account.id = :id "
            "GROUP BY Laji.nimi "
            "ORDER BY maara DESC;").params(
            id=userId)

        res = db.engine.execute(stmt)

        return res
