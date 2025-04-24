from app.models import db
from datetime import datetime

class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    amount = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    goods_id = db.Column(db.Integer)  # Optional: link to RawStock or ProcessedStock
    date_issued = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(255))  # Purpose or reason

    supplier = db.relationship("Supplier", back_populates="debts")