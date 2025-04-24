from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Machinery, MachineryExpense
from datetime import datetime

machinery_bp = Blueprint("machinery", __name__)

@machinery_bp.route("/")
def list_machines():
    machines = Machinery.query.all()
    return render_template("machinery/list.html", machines=machines)

@machinery_bp.route("/add", methods=["GET", "POST"])
def add_machinery():
    if request.method == "POST":
        name = request.form["name"]
        type_ = request.form["type"]
        last_service = datetime.strptime(request.form["last_service"], "%Y-%m-%d")
        next_service = datetime.strptime(request.form["next_service"], "%Y-%m-%d")

        machine = Machinery(
            name=name,
            type=type_,
            last_service_date=last_service,
            next_service_due=next_service
        )
        db.session.add(machine)
        db.session.commit()
        return redirect(url_for("machinery.list_machines"))

    return render_template("machinery/add.html")

@machinery_bp.route("/<int:machinery_id>/expense", methods=["GET", "POST"])
def add_expense(machinery_id):
    machine = Machinery.query.get_or_404(machinery_id)

    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        description = request.form["description"]
        date = datetime.now()

        expense = MachineryExpense(
            machinery_id=machine.id,
            category=category,
            amount=amount,
            description=description,
            date=date
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for("machinery.list_machines"))

    return render_template("machinery/expense_add.html", machine=machine)
