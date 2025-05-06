from . import db

class Machinery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # Grinder, Separator, etc.

    last_service_date = db.Column(db.Date)
    next_service_due = db.Column(db.Date)

    expenses = db.relationship('MachineryExpense', backref='machinery', lazy=True , cascade = 'all,delete-orphan')
    services = db.relationship('ServiceSchedule', backref='machinery', lazy=True)
