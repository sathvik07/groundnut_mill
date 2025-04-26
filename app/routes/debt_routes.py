from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app.models import db, Supplier, Debt
from datetime import datetime

debt_bp = Blueprint("debt", __name__)

@debt_bp.route("/debts")
@login_required
def list_debts():
    debts = Debt.query.order_by(Debt.date_issued.desc()).all()
    return render_template("debt/list.html", debts=debts)

@debt_bp.route("/debts/add", methods=["GET", "POST"])
@login_required
def add_debt():
    suppliers = Supplier.query.all()

    if request.method == "POST":
        supplier_id = request.form["supplier_id"]
        amount = float(request.form["amount"])
        total_cost = float(request.form.get("total_cost") or 0)
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

        return redirect(url_for("debt.list_debts"))

    return render_template("debt/add.html", suppliers=suppliers)
