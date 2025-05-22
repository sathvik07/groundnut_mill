from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError

from app.models import db
from app.models.supplier import Supplier
from datetime import datetime

supplier_bp = Blueprint("supplier", __name__)

@supplier_bp.route("/")
@login_required
def list_suppliers():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    try:
        pagination = Supplier.query.order_by(Supplier.name).paginate(page=page, per_page=per_page)
        return render_template("suppliers/list.html", pagination=pagination)
        # suppliers = Supplier.query.all()
    except SQLAlchemyError as e:
        flash("Error retrieving suppliers", "error")
        current_app.logger.error(f"Error retrieving suppliers: {e}")
        # Consider logging the error: logger.error(f"Error retrieving suppliers: {e}")
        # Handle the error (e.g., log it, flash a message, etc.)
        # return render_template("suppliers/list.html", suppliers=[])
        suppliers = []
    return render_template("suppliers/list.html", suppliers=suppliers)


@supplier_bp.route("/search", methods=["GET"])
@login_required
def search_suppliers():
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 20

    try:
        query = Supplier.query
        if search_query:
            query = query.filter(Supplier.name.ilike(f"%{search_query}%"))

        pagination = query.order_by(Supplier.name).paginate(page=page, per_page=per_page)
        return render_template("suppliers/search.html", pagination=pagination, search_query=search_query)
    except SQLAlchemyError as e:
        flash("Error searching suppliers", "error")
        current_app.logger.error(f"Error searching suppliers: {e}")
        return render_template("suppliers/search.html", pagination=None, search_query=search_query)


@supplier_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_supplier():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            contact = request.form.get("contact")
            type_ = request.form.get("type")

            if not all([name, contact, type_]):
                flash("All fields are required", "error")
                current_app.logger.warning("Supplier form submission failed: Missing fields.")
                return render_template("suppliers/add.html")

            supplier = Supplier(name=name, contact=contact, type=type_)
            db.session.add(supplier)
            db.session.commit()
            flash("Supplier added successfully", "success")
            current_app.logger.info(f"Supplier added: {supplier.id} - {supplier.name}")
            return redirect(url_for("raw_stock.add_raw_stock"))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Error adding supplier", "error")
            current_app.logger.error(f"Error adding supplier: {e}")
            return render_template("suppliers/add.html"), 500

    return render_template("suppliers/add.html")


@supplier_bp.route("/edit/<int:supplier_id>", methods=["GET", "POST"])
@login_required
def edit_supplier(supplier_id):
    try:
        supplier = Supplier.query.get_or_404(supplier_id)

        if request.method == "POST":
            supplier.name = request.form["name"]
            supplier.contact = request.form["contact"]
            supplier.type = request.form["type"]
            if not all([request.form.get("name"), request.form.get("contact"), request.form.get("type")]):
                flash("All fields are required", "error")
                current_app.logger.warning("Supplier form submission failed: Missing fields.")
                return render_template("suppliers/edit.html", supplier=supplier)
            db.session.commit()
            flash("Supplier updated successfully", "success")
            current_app.logger.info(f"Supplier updated: {supplier.id} - {supplier.name}")
            return redirect(url_for("supplier.list_suppliers"))

        return render_template("suppliers/edit.html", supplier=supplier)
    except SQLAlchemyError as e:
        db.session.rollback()
        flash("Error updating supplier", "error")
        current_app.logger.error(f"Error updating supplier: {e}")
        # Consider logging the error: logger.error(f"Error updating supplier: {e}")
        return redirect(url_for("supplier.list_suppliers"))

@supplier_bp.route("/delete/<int:supplier_id>", methods=["DELETE", "POST"])
@login_required
def delete_supplier(supplier_id):
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        db.session.delete(supplier)
        db.session.commit()
        flash("Supplier deleted successfully", "success")
        current_app.logger.info(f"Supplier deleted: {supplier.id} - {supplier.name}")
        return redirect(url_for("supplier.list_suppliers"))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash("Error deleting supplier", "error")
        current_app.logger.error(f"Error deleting supplier: {e}")
        return redirect(url_for("supplier.list_suppliers"))



@supplier_bp.route("/<int:supplier_id>/debts", methods=["GET", "POST"])
@login_required
def list_debt_by_supplier_id(supplier_id):
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        debts = supplier.debts.all()
        return render_template("debt/list_by_supplier.html", supplier=supplier, debts=debts)
    except SQLAlchemyError as e:
        flash("Error retrieving supplier debts", "error")
        current_app.logger.error(f"Error retrieving supplier debts: {e}")
        # Consider logging the error: logger.error(f"Error retrieving supplier debts: {e}")
        return redirect(url_for("supplier.list_suppliers"))


