from flask import Blueprint, render_template
from flask_login import login_required

from app.models import db, RawStock, ProcessedStock, Debt, VehicleExpense, MachineryExpense, Supplier, Vehicle, Machinery
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def dashboard():
    total_raw_weight = db.session.query(func.sum(RawStock.weight_kg)).scalar() or 0
    total_processed_weight = db.session.query(func.sum(ProcessedStock.quantity_kg)).scalar() or 0
    total_debt = db.session.query(func.sum(Debt.amount)).scalar() or 0

    vehicle_expenses = db.session.query(func.sum(VehicleExpense.amount)).scalar() or 0
    machinery_expenses = db.session.query(func.sum(MachineryExpense.amount)).scalar() or 0

    supplier_count = Supplier.query.count()
    vehicle_count = Vehicle.query.count()
    machinery_count = Machinery.query.count()

    # Data for Charts
    raw_vs_processed = {
        "raw": total_raw_weight,
        "processed": total_processed_weight
    }

    expenses = {
        "vehicle": vehicle_expenses,
        "machinery": machinery_expenses
    }

    return render_template("dashboard/index.html",
        total_raw_weight=total_raw_weight,
        total_processed_weight=total_processed_weight,
        total_debt=total_debt,
        vehicle_expenses=vehicle_expenses,
        machinery_expenses=machinery_expenses,
        supplier_count=supplier_count,
        vehicle_count=vehicle_count,
        machinery_count=machinery_count,
        raw_vs_processed=raw_vs_processed,
        expenses=expenses
    )
