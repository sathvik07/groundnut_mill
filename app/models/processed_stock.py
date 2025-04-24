from . import db

class ProcessedStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_stock_id = db.Column(db.Integer, db.ForeignKey('raw_stock.id'), nullable=False)
    expected_weight = db.Column(db.Float)
