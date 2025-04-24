from . import db

class Distributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))
    address = db.Column(db.String(200))
    # One-to-many with Sales
    sales = db.relationship('Sale', backref='distributor', lazy=True)
