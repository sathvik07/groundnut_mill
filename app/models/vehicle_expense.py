from . import db
from datetime import datetime

class VehicleExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)
    notes = db.Column(db.String(255))  # New column

    vehicle = db.relationship("Vehicle", back_populates="expenditures")
