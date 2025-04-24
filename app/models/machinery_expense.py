from . import db

class MachineryExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machinery_id = db.Column(db.Integer, db.ForeignKey('machinery.id'), nullable=False)
    category = db.Column(db.String(50))  # Spare Parts, Repair, etc.
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(200))
