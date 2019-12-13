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
    def find_saalis(saalis_id, user_id):
        stmt = text(
            "SELECT Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Sijainti.alue, Laji.nimi, Saalis.julkinen "
            "FROM Saalis "
            "JOIN Account ON Saalis.account_id = account.id "
            "JOIN Sijainti ON Saalis.sijainti_id = sijainti.id "
            "JOIN Laji ON Saalis.laji_id = laji.id "
            "WHERE Account.id = :user_id "
            "AND Saalis.id = :saalis_id").params(user_id=user_id, saalis_id=saalis_id)
        res = db.engine.execute(stmt)

        return res.first()

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


class Jaot(db.Model):
    jakaja_account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)
    kohde_account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), primary_key=True, nullable=False)
    jaettu_saalis_id = db.Column(db.Integer, db.ForeignKey(
        'saalis.id'), primary_key=True, nullable=False)

    def __init__(self, creator_account_id, target_account_id, shared_saalis_id):
        self.jakaja_account_id = creator_account_id
        self.kohde_account_id = target_account_id
        self.jaettu_saalis_id = shared_saalis_id

    @staticmethod
    def get_users_shares(saalis_id):
        stmt = text(
            "SELECT Account.id AS target_id, Account.username AS target_username "
            "FROM Jaot "
            "JOIN Account ON Jaot.kohde_account_id = account.id "
            "WHERE jaettu_saalis_id = :id ").params(id=saalis_id)
        res = db.engine.execute(stmt)
        return res

    @staticmethod
    def delete_share(kohde_account_id, jaettu_saalis_id):
        stmt = text(
            "DELETE FROM Jaot "
            "WHERE kohde_account_id = :kohde_account_id AND jaettu_saalis_id = :jaettu_saalis_id ").params(
            jaettu_saalis_id=jaettu_saalis_id, kohde_account_id=kohde_account_id)
        db.engine.execute(stmt)

    @staticmethod
    def get_shared_to_user(user_id):
        stmt = text(
            "SELECT Account.username, Saalis.id, Saalis.account_id, Saalis.maara, Saalis.koordinaatit, Saalis.paivamaara, Saalis.julkinen, Sijainti.alue, Laji.nimi, Saalis.julkinen "
            "FROM Jaot "
            "JOIN Saalis ON Jaot.jaettu_saalis_id = Saalis.id "
            "JOIN Account ON Saalis.account_id = Account.id "
            "JOIN Sijainti ON Saalis.sijainti_id = sijainti.id "
            "JOIN Laji ON Saalis.laji_id = laji.id "
            "WHERE kohde_account_id = :id ").params(id=user_id)

        res = db.engine.execute(stmt)
        return res

    @staticmethod
    def delete_users_shares(user_id):
        stmt = text(
            "DELETE FROM Jaot "
            "WHERE Jaot.jakaja_account_id = :id ").params(id=user_id)
        db.engine.execute(stmt)
