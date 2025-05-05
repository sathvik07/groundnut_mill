from flask import Blueprint, render_template
from flask_login import login_required

from app.models import ProcessedStock, db

processed_stock_bp = Blueprint("processed_stock", __name__)

from sqlalchemy import func

@processed_stock_bp.route("/processed")
@login_required
def view_processed_stock():
    total_stock = db.session.query(func.sum(ProcessedStock.quantity_kg)).scalar() or 0.0
    return render_template("processed_stock/list.html", total_stock=total_stock)

