from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app.models import db
from app.models.supplier import Supplier
from datetime import datetime

supplier_bp = Blueprint("supplier", __name__)

@supplier_bp.route("/")
@login_required
def list_suppliers():
    suppliers = Supplier.query.all()
    return render_template("suppliers/list.html", suppliers=suppliers)

@supplier_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_supplier():
    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        type_ = request.form["type"]

        supplier = Supplier(name=name, contact=contact, type=type_)
        db.session.add(supplier)
        db.session.commit()
        return redirect(url_for("supplier.list_suppliers"))

    return render_template("suppliers/add.html")



@supplier_bp.route("/edit/<int:supplier_id>", methods=["GET", "POST"])
@login_required
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)

    if request.method == "POST":
        supplier.name = request.form["name"]
        supplier.contact = request.form["contact"]
        supplier.type = request.form["type"]

        db.session.commit()
        return redirect(url_for("supplier.list_suppliers"))

    return render_template("suppliers/edit.html", supplier=supplier)


@supplier_bp.route("/delete/<int:supplier_id>")
@login_required
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return redirect(url_for("supplier.list_suppliers"))



@supplier_bp.route("/<int:supplier_id>/debts", methods=["GET", "POST"])
@login_required
def list_debt_by_supplier_id(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    debts = supplier.debts.all()
    return render_template("debt/list_by_supplier.html", supplier=supplier, debts=debts)


