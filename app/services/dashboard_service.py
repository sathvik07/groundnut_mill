# app/services/dashboard_service.py
from app.models import db, RawStock, ProcessedStock, Debt, VehicleExpense, MachineryExpense, Supplier, Vehicle, Machinery
from sqlalchemy import func

def get_dashboard_metrics():
    return {
        "total_raw_weight": db.session.query(func.sum(RawStock.weight_kg)).scalar() or 0,
        "total_processed_weight": db.session.query(func.sum(ProcessedStock.quantity_kg)).scalar() or 0,
        "total_debt": db.session.query(func.sum(Debt.amount)).scalar() or 0,
        "vehicle_expenses": db.session.query(func.sum(VehicleExpense.amount)).scalar() or 0,
        "machinery_expenses": db.session.query(func.sum(MachineryExpense.amount)).scalar() or 0,
        "supplier_count": Supplier.query.count(),
        "vehicle_count": Vehicle.query.count(),
        "machinery_count": Machinery.query.count()
    }
