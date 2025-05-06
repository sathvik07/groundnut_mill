from flask import Blueprint, render_template, current_app
from flask_login import login_required
from app import cache

from app.models import db, RawStock, ProcessedStock, Debt, VehicleExpense, MachineryExpense, Supplier, Vehicle, Machinery
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__)

from app.services.dashboard_service import get_dashboard_metrics

@dashboard_bp.route("/")
@login_required
@cache.cached(timeout=300, key_prefix='dashboard_data')
def dashboard():
    metrics = get_dashboard_metrics()

    raw_vs_processed = {
        "raw": metrics["total_raw_weight"],
        "processed": metrics["total_processed_weight"]
    }

    expenses = {
        "vehicle": metrics["vehicle_expenses"],
        "machinery": metrics["machinery_expenses"]
    }

    return render_template("dashboard/index.html", **metrics, raw_vs_processed=raw_vs_processed, expenses=expenses)

