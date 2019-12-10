from sqlalchemy.sql import text

from application import db


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

    @staticmethod
    def find_maarat_alueittain_by_user_id(userId):
        stmt = text(
            "SELECT Sijainti.alue, SUM(Saalis.maara) AS maara "
            "FROM Sijainti "
            "LEFT JOIN Saalis ON Sijainti.id = Saalis.sijainti_id "
            "JOIN Account ON Saalis.account_id = account.id "
            "WHERE Account.id = :id "
            "GROUP BY Sijainti.alue "
            "ORDER BY maara DESC;").params(
            id=userId)

        res = db.engine.execute(stmt)

        return res
