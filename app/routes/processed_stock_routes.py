from flask import Blueprint, render_template
from app.models import ProcessedStock

processed_stock_bp = Blueprint("processed_stock", __name__)

@processed_stock_bp.route("/processed")
def view_processed_stock():
    processed_stocks = ProcessedStock.query.all()
    return render_template("processed_stock/list.html", processed_stocks=processed_stocks)
