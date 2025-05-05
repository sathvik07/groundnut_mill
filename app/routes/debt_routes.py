import werkzeug
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app import cache  # Import the cache instance
from app.models import db, Supplier, Debt
from datetime import datetime

debt_bp = Blueprint("debt", __name__)

def safe_cache_operation(operation):
    try:
        return operation()
    except Exception as e:
        current_app.logger.error(f"Cache operation failed: {e}")
        return None

# Usage:
@debt_bp.route("/debts")
@login_required
def list_debts():
    cached_data = safe_cache_operation(
        lambda: current_app.cache.get(f'debt_list_{request.query_string}')
    )
    if cached_data:
        return cached_data
    page = request.args.get('page', 1, type=int)
    per_page = 10
    sort_by = request.args.get('sort', 'date_issued')
    order = request.args.get('order', 'desc')
    
    query = Debt.query
    
    if sort_by == 'amount':
        query = query.order_by(Debt.amount.desc() if order == 'desc' else Debt.amount)
    else:  # default to date_issued
        query = query.order_by(Debt.date_issued.desc() if order == 'desc' else Debt.date_issued)
        
    debts = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("debt/list.html", debts=debts, sort_by=sort_by, order=order)

@debt_bp.route("/debts/add", methods=["GET", "POST"])
@login_required
def add_debt():
    suppliers = Supplier.query.all()

    if request.method == "POST":
        try:
            supplier_id = request.form["supplier_id"]
            supplier = Supplier.query.get(supplier_id)
            if not supplier:
                flash("Selected supplier does not exist", "danger")
                return render_template("debt/add.html", suppliers=suppliers)

            amount = float(request.form["amount"])
            total_cost = float(request.form.get("total_cost") or 0)

            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            if total_cost < 0:
                raise ValueError("Total cost cannot be negative")

            notes = request.form.get("notes")
            date_issued = datetime.now()
    
            debt = Debt(
                supplier_id=supplier_id,
                amount=amount,
                total_cost=total_cost,
                notes=notes,
                date_issued=date_issued
            )
            db.session.add(debt)
            db.session.commit()
            
            # Clear relevant caches
            current_app.cache.delete('debt_list_view')
            current_app.cache.delete(f'supplier_debts_{supplier_id}')
            
            flash("Debt added successfully!", "success")
            
            # Clear all related caches
            current_app.cache.delete_memoized(list_debts)
            current_app.cache.delete_memoized(list_debt_by_supplier_name)
            current_app.cache.delete_memoized(list_debt_by_supplier_id)
            
            return redirect(url_for("debt.list_debts"))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("debt/add.html", suppliers=suppliers)
        except Exception as e:
            flash(f"Error adding debt: {str(e)}", "danger")
            return render_template("debt/add.html", suppliers=suppliers)

    return render_template("debt/add.html", suppliers=suppliers)

@debt_bp.route("/debts/list/<supplier_name>")
@login_required
@cache.cached(timeout=300, query_string=True)  # Use cache. instead of current_app.cache
def list_debt_by_supplier_name(supplier_name):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        supplier = Supplier.query.filter_by(name=supplier_name).first_or_404()
        debts = Debt.query.filter_by(supplier_id=supplier.id).paginate(
            page=page, per_page=per_page, error_out=False)
        return render_template("debt/list_by_supplier.html", supplier=supplier, debts=debts)
    except werkzeug.exceptions.NotFound:
        flash(f"Supplier '{supplier_name}' not found", "danger")
        return redirect(url_for("debt.list_debts"))
    except SQLAlchemyError as e:
        flash(f"Database error occurred: {str(e)}", "danger")
        return redirect(url_for("debt.list_debts"))

@debt_bp.route("/debts/list/<int:supplier_id>")
@login_required
@cache.cached(timeout=300, query_string=True)  # Use cache. instead of current_app.cache
def list_debt_by_supplier_id(supplier_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        supplier = Supplier.query.get_or_404(supplier_id)
        debts = Debt.query.filter_by(supplier_id=supplier.id).paginate(
            page=page, per_page=per_page, error_out=False)
        return render_template("debt/list_by_supplier.html", supplier=supplier, debts=debts)
    except werkzeug.exceptions.NotFound:
        flash(f"Supplier '{supplier_id}' not found", "danger")
        return redirect(url_for("debt.list_debts"))
    except SQLAlchemyError as e:
        flash(f"Database error occurred: {str(e)}", "danger")
        return redirect(url_for("debt.list_debts"))

@debt_bp.route("/debts/search")
@login_required
def search_debts():
    # Search results are not cached as they are dynamic
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    if query:
        debts = Debt.query.join(Supplier).filter(
            (Supplier.name.ilike(f'%{query}%')) |
            (Debt.notes.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        debts = Debt.query.paginate(page=page, per_page=per_page, error_out=False)
        
    return render_template("debt/list.html", debts=debts, search_query=query)

@debt_bp.after_request
def add_cache_headers(response):
    if request.endpoint in ['debt.list_debts', 'debt.list_debt_by_supplier_id']:
        response.headers['Cache-Control'] = 'public, max-age=300'
    else:
        response.headers['Cache-Control'] = 'no-store'
    return response