from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models.sale import Sale
from app.models.distributor import Distributor
from app.models.processed_stock import ProcessedStock
from flask_login import login_required

sale_bp = Blueprint('sale', __name__, url_prefix='/sale')

@sale_bp.route('/')
@login_required
def list_sales():
    sales = Sale.query.all()
    return render_template('sales/list.html', sales=sales)

@sale_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_sale():
    distributors = Distributor.query.all()
    processed_stocks = ProcessedStock.query.all()  # Available processed stock

    if request.method == "POST":
        try:
            distributor_id = int(request.form["distributor_id"])
            processed_stock_id = int(request.form["processed_stock_id"])
            quantity_sold = float(request.form["quantity_sold"])
            price_per_kg = float(request.form["price_per_kg"])

            # Find the processed stock item being sold
            processed_stock = ProcessedStock.query.get(processed_stock_id)

            # Check if there's enough stock to sell
            if processed_stock.quantity_kg < quantity_sold:
                flash("Not enough processed stock to complete the sale.", "danger")
                return redirect(url_for("sale.add_sale"))

            # Calculate total price
            total_price = price_per_kg * quantity_sold

            # Create Sale entry
            sale = Sale(
                distributor_id=distributor_id,
                processed_stock_id=processed_stock_id,
                quantity_sold=quantity_sold,
                price_per_kg=price_per_kg,
                total_price=total_price
            )
            db.session.add(sale)

            # Update processed stock quantity
            processed_stock.quantity_kg -= quantity_sold

            db.session.commit()
            flash("Sale completed successfully!", "success")
            return redirect(url_for("sale.list_sales"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error processing sale: {str(e)}", "danger")

    return render_template("sales/add.html", distributors=distributors, processed_stocks=processed_stocks)


@sale_bp.route('/delete/<int:sale_id>')
@login_required
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    flash('Sale deleted successfully.', 'info')
    return redirect(url_for('sale.list_sales'))
