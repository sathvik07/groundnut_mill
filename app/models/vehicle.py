from app.models import db

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number_plate = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    expenditures = db.relationship("VehicleExpense", back_populates="vehicle", cascade="all, delete")

