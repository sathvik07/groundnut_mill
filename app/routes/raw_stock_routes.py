from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, RawStock, ProcessedStock, Supplier
from datetime import datetime

raw_stock_bp = Blueprint("raw_stock", __name__)

@raw_stock_bp.route("/")
def list_raw_stock():
    stocks = RawStock.query.all()
    return render_template("raw_stock/list.html", stocks=stocks)

@raw_stock_bp.route("/add", methods=["GET", "POST"])
def add_raw_stock():
    suppliers = Supplier.query.all()

    if request.method == "POST":
        supplier_id = request.form["supplier_id"]
        weight = float(request.form["weight"])
        gram = int(request.form["gram"])
        date = datetime.now()

        # Create raw stock
        raw_stock = RawStock(
            supplier_id=supplier_id,
            weight_kg=weight,
            gram=gram,
            date=date
        )
        db.session.add(raw_stock)
        db.session.flush()  # get raw_stock.id before commit

        # Calculate expected processed weight
        expected = weight * (gram / 100)
        processed = ProcessedStock(
            raw_stock_id=raw_stock.id,
            expected_weight=expected
        )
        db.session.add(processed)
        db.session.commit()

        return redirect(url_for("raw_stock.list_raw_stock"))

    return render_template("raw_stock/add.html", suppliers=suppliers)
