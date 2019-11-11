from application import db

class Saalis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    laji = db.Column(db.String(100), nullable=False)
    paikka = db.Column(db.String(100), nullable=False)
    paivamaara = db.Column(db.DateTime, default=db.func.current_timestamp())
    maara = db.Column(db.Integer, nullable=False)
    koordinaatit = db.Column(db.String(100), nullable=False)
    
    def __init__(self,laji,paikka,maara,koordinaatit):
        self.laji = laji
        self.paikka = paikka
        self.maara = maara
        self.koordinaatit = koordinaatit