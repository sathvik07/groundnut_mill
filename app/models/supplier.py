from . import db

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # Farmer, Broker, etc.
    contact = db.Column(db.String(100))

    raw_stocks = db.relationship('RawStock', backref='supplier', lazy=True)
    debts = db.relationship("Debt", back_populates="supplier", cascade="all, delete")
