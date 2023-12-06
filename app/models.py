from app import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), index=True, unique=True)
    IP = db.Column(db.String(256))
