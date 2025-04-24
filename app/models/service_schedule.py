from . import db

class ServiceSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machinery_id = db.Column(db.Integer, db.ForeignKey('machinery.id'), nullable=False)
    service_date = db.Column(db.DateTime)
    notes = db.Column(db.String(200))
