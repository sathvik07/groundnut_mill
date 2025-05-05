from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime

from app.models import db, RawStock, ProcessedStock, Supplier

raw_stock_bp = Blueprint("raw_stock", __name__)

@raw_stock_bp.route("/")
@login_required
def list_raw_stock():
    stocks = RawStock.query.all()
    return render_template("raw_stock/list.html", stocks=stocks)

@raw_stock_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_raw_stock():
    suppliers = Supplier.query.all()

    if request.method == "POST":
        try:
            supplier_id = int(request.form["supplier_id"])
            weight_kg = float(request.form["weight"])
            gram = int(request.form["gram"])

            if gram < 0 or gram > 100:
                flash("Gram value must be between 0 and 100.", "danger")
                return redirect(url_for("raw_stock.add_raw_stock"))

            # Create RawStock entry
            raw_stock = RawStock(
                supplier_id=supplier_id,
                weight_kg=weight_kg,
                gram=gram,
                date=datetime.utcnow()
            )
            db.session.add(raw_stock)

            # Calculate expected processed stock
            expected_processed_weight = weight_kg * (gram / 100)

            # Add ProcessedStock entry
            processed_stock = ProcessedStock(
                product_name="Processed Groundnut Oil",  # Example product
                quantity_kg=expected_processed_weight
            )
            db.session.add(processed_stock)

            db.session.commit()
            flash("Raw stock and processed stock added successfully!", "success")
            return redirect(url_for("raw_stock.list_raw_stock"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error adding stock: {str(e)}", "danger")

    return render_template("raw_stock/add.html", suppliers=suppliers)



@raw_stock_bp.route("/<int:supplier_id>", methods=["GET", "POST"])
@login_required
def display_processed_stock(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    stocks = RawStock.query.filter_by(supplier_id=supplier.id).all()
    return render_template("raw_stock/supplier_pro_stock.html", supplier=supplier, stocks=stocks)
