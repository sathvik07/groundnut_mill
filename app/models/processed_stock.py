# from . import db
#
# class ProcessedStock(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     raw_stock_id = db.Column(db.Integer, db.ForeignKey('raw_stock.id'), nullable=False)
#     expected_weight = db.Column(db.Float)
from datetime import datetime
from enum import unique

from . import db

class ProcessedStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False, unique=True)
    quantity_kg = db.Column(db.Float, nullable=False, default=0.0)  # Track available stock
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Sales relationship
    # sales = db.relationship('Sale', backref='processed_stock', lazy=True)