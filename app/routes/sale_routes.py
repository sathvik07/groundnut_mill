from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.sale import Sale
from app.models.distributor import Distributor
from app.models.processed_stock import ProcessedStock
from flask_login import login_required

sale_bp = Blueprint('sale', __name__, url_prefix='/sale')

@sale_bp.route('/')
@login_required
def list_sales():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    try:
        pagination = Sale.query.order_by(Sale.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
        # sales = Sale.query.all()
        return render_template('sales/list.html', sales=sales)
    except Exception as e:
        # Handle the error (e.g., log it, flash a message, etc.)
        flash("Error retrieving sales.", "error")
        # Consider logging the error: logger.error(f"Error retrieving sales: {e}")
        return render_template('sales/list.html', sales=[])

@sale_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_sale():
    distributors = Distributor.query.all()
    processed_stock = ProcessedStock.query.first()
    
    if not processed_stock:
        flash("No processed stock record found.", "danger")
        return redirect(url_for("sale.list_sales"))

    if request.method == "POST":
        try:
            with db.session.begin_nested():  # Creates a savepoint
                distributor_id = int(request.form["distributor_id"])
                quantity_sold = float(request.form["quantity_sold"])
                price_per_kg = float(request.form["price_per_kg"])

                if quantity_sold <= 0 or price_per_kg <= 0:
                    flash("Quantity and price must be positive values.", "danger")
                    return redirect(url_for("sale.add_sale"))

                distributor = Distributor.query.get(distributor_id)
                if not distributor:
                    flash("Invalid distributor selected.", "danger")
                    return redirect(url_for("sale.add_sale"))

                # Requery the stock for the latest value
                processed_stock = ProcessedStock.query.with_for_update().first()
                if not processed_stock or processed_stock.quantity_kg < quantity_sold:
                    flash("Not enough processed stock to complete the sale.", "danger")
                    return redirect(url_for("sale.add_sale"))
            total_price = price_per_kg * quantity_sold

            # Create a Sale entry
            sale = Sale(
                distributor_id=distributor_id,
                quantity_sold=quantity_sold,
                price_per_kg=price_per_kg,
                total_price=total_price
            )
            db.session.add(sale)

            # Subtract from global processed stock
            processed_stock.quantity_kg -= quantity_sold

            db.session.commit()
            flash("Sale completed successfully!", "success")
            return redirect(url_for("sale.list_sales"))

        except ValueError:
            flash("Invalid input values provided.", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("Database integrity error occurred.", "danger")
        except Exception as e:
            db.session.rollback()
            # Log the actual error for debugging
            # current_app.logger.error(f"Sale processing error: {str(e)}")
            flash("An unexpected error occurred. Please try again.", "danger")

    return render_template("sales/add.html", distributors=distributors, processed_stock=processed_stock)



@sale_bp.route('/delete/<int:sale_id>', methods=["DELETE", "POST"])
@login_required
def delete_sale(sale_id):
    try:
        sale = Sale.query.get_or_404(sale_id)
        db.session.delete(sale)
        db.session.commit()
        flash('Sale deleted successfully.', 'info')
        return redirect(url_for('sale.list_sales'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting sale: {str(e)}', 'danger')
        return redirect(url_for('sale.list_sales'))