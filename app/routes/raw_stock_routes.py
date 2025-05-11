from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from datetime import datetime
import logging
from contextlib import contextmanager

from app.models import db, RawStock, ProcessedStock, Supplier
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

raw_stock_bp = Blueprint("raw_stock", __name__)

@contextmanager
def db_transaction():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

@raw_stock_bp.route("/")
@login_required
def list_raw_stock():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    try:
        pagination = RawStock.query.order_by(RawStock.date.desc()).paginate(page=page, per_page=per_page)
        return render_template("raw_stock/list.html", pagination=pagination)
    except SQLAlchemyError as e:
        # logger.error(f"Database error in list_raw_stock: {str(e)}")
        flash("Error fetching stock data", "error")
        current_app.logger.error(f"Database error in list_raw_stock: {str(e)}")
        return render_template("raw_stock/list.html", pagination=None)


@raw_stock_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_raw_stock():
    """Add new raw stock and calculate the corresponding processed stock."""
    try:
        suppliers = Supplier.query.all()
        if not suppliers:
            flash("No suppliers available. Please add suppliers first.", "warning")
            current_app.logger.warning("No suppliers available. Redirecting to supplier add page.")
            return redirect(url_for("supplier.add_supplier"))

        if request.method == "POST":
            try:
                supplier_id = int(request.form["supplier_id"])
                weight_kg = float(request.form["weight"])
                gram = int(request.form["gram"])

                # Input validation
                if not Supplier.query.get(supplier_id):
                    flash("Invalid supplier selected.", "danger")
                    current_app.logger.warning(f"Invalid supplier selected: {supplier_id}")
                    return redirect(url_for("raw_stock.add_raw_stock"))
                
                if weight_kg <= 0:
                    flash("Weight must be greater than 0.", "danger")
                    current_app.logger.warning(f"Invalid weight value: {weight_kg}")
                    return redirect(url_for("raw_stock.add_raw_stock"))

                if gram < 0 or gram > 100:
                    flash("Gram value must be between 0 and 100.", "danger")
                    current_app.logger.warning(f"Invalid gram value: {gram}")
                    return redirect(url_for("raw_stock.add_raw_stock"))

                with db_transaction():
                    raw_stock = RawStock(
                        supplier_id=supplier_id,
                        weight_kg=weight_kg,
                        gram=gram,
                        date=datetime.utcnow()
                    )
                    db.session.add(raw_stock)

                    expected_processed_weight = weight_kg * (gram / 100)
                    processed_stock = ProcessedStock(
                        product_name="Processed Groundnut",
                        quantity_kg=expected_processed_weight,
                        created_at=datetime.utcnow()
                    )
                    db.session.add(processed_stock)

                flash("Raw stock and processed stock added successfully!", "success")
                # current_app.logger.error()
                return redirect(url_for("raw_stock.list_raw_stock"))

            except ValueError:
                flash("Please ensure all input values are valid numbers", "danger")
                current_app.logger.warning("Invalid input values in add_raw_stock.")
            except SQLAlchemyError as e:
                flash("Database error occurred", "danger")
                current_app.logger.error(f"Database error in add_raw_stock: {str(e)}")
            except Exception as e:
                flash("An unexpected error occurred", "danger")
                current_app.logger.error(f"Unexpected error in add_raw_stock: {str(e)}")

        return render_template("raw_stock/add.html", suppliers=suppliers)
    except SQLAlchemyError as e:
        flash("Error fetching suppliers data", "error")
        current_app.logger.error(f"Database error fetching suppliers: {str(e)}")
        return redirect(url_for("raw_stock.list_raw_stock"))

@raw_stock_bp.route("/<int:supplier_id>", methods=["GET"])
@login_required
def list_supplier_raw_stock(supplier_id):
    """List all raw stock entries for a specific supplier."""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        stocks = RawStock.query.filter_by(supplier_id=supplier.id).order_by(RawStock.date.desc()).all()
        return render_template("raw_stock/supplier_pro_stock.html", supplier=supplier, stocks=stocks)
    except SQLAlchemyError as e:
        logger.error(f"Database error in list_supplier_raw_stock: {str(e)}")
        flash("Error fetching supplier stock data", "error")
        current_app.logger.error(f"Database error in list_supplier_raw_stock: {str(e)}")
        return render_template("raw_stock/supplier_pro_stock.html", supplier=None, stocks=[])