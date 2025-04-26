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
