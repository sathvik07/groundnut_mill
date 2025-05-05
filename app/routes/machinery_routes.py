from flask import Blueprint, render_template, request, redirect, url_for ,flash
from flask_login import login_required

from app.models import db, Machinery, MachineryExpense
from datetime import datetime

machinery_bp = Blueprint("machinery", __name__)

@machinery_bp.route("/")
@login_required
def list_machines():
    machines = Machinery.query.all()
    return render_template("machinery/list.html", machines=machines)

@machinery_bp.route("/add", methods=["GET", "POST"])
@login_required
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

@machinery_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_machinery(id):
    machinery = Machinery.query.get_or_404(id)
    print(machinery.name)
    if request.method == "POST":
        new_name = request.form["name"]
        new_machine_type = request.form["type"]  # or whatever your form input is named
        last_service_input = request.form.get("last_service_date", "").strip()
        next_service_input = request.form.get("next_service_due", "").strip()

        # Update fields correctly
        machinery.name = new_name      # <-- Updated to match model
        machinery.type = new_machine_type  # <-- Updated to match model

        if last_service_input:
            try:
                machinery.last_service_date = datetime.strptime(last_service_input, "%Y-%m-%d")
            except ValueError:
                flash("Invalid Last Service date format.", "danger")
                return redirect(request.url)

        if next_service_input:
            try:
                machinery.next_service_due = datetime.strptime(next_service_input, "%Y-%m-%d")
            except ValueError:
                flash("Invalid Next Service Due date format.", "danger")
                return redirect(request.url)

        try:
            db.session.commit()
            flash("Machinery updated successfully!", "success")
            return redirect(url_for("machinery.list_machines"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating machinery: {str(e)}", "danger")

    return render_template("machinery/edit_machinery_info.html", machinery=machinery)