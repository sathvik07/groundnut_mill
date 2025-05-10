from flask import Blueprint, render_template, flash, current_app
from flask_login import login_required
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.models import ProcessedStock, db

processed_stock_bp = Blueprint("processed_stock", __name__)

@processed_stock_bp.route("/processed")
@login_required
def view_processed_stock() -> str:
    try:
        total_stock = db.session.query(func.sum(ProcessedStock.quantity_kg)).scalar() or 0.0
        return render_template("processed_stock/list.html", total_stock=total_stock)
    except SQLAlchemyError as e:
        flash("Error fetching stock data", "error")
        current_app.logger.error(f"Error fetching stock data: {e}")
        return render_template("processed_stock/list.html", total_stock=0.0)


