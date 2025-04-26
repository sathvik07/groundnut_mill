from datetime import datetime

from . import db

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributor.id'), nullable=False)
    processed_stock_id = db.Column(db.Integer, db.ForeignKey('processed_stock.id'), nullable=False)
    quantity_sold = db.Column(db.Float, nullable=False)
    price_per_kg = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date_sold = db.Column(db.DateTime, default=datetime.utcnow)
