from . import db

class RawStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    gram = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)

    processed_stock = db.relationship('ProcessedStock', backref='raw_stock', uselist=False)
