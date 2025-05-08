import decimal
from typing import Optional
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
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

@machinery_bp.route("/<int:id>/expense", methods=["GET", "POST"])
@login_required
def add_expense(id: int):
    machine = Machinery.query.get_or_404(id)

    if request.method == "POST":
        try:
            amount = Decimal(request.form["amount"])
            if amount <= 0:
                raise ValueError("Amount must be positive")

            category = request.form.get("category", "").strip()
            description = request.form.get("description", "").strip()

            if not all([category, description]):
                flash("All fields are required", "error")
                current_app.logger.warning("Expense form submission failed: Missing fields.")
                return redirect(request.url)

            expense = MachineryExpense(
                machinery_id=machine.id,
                category=category,
                amount=amount,
                description=description,
                date=datetime.now()
            )
            db.session.add(expense)
            db.session.commit()
            flash("Expense added successfully!", "success")
            current_app.logger.info(f"Expense added for machinery ID {id}")
            return redirect(url_for("machinery.list_machines"))

        except (ValueError, decimal.InvalidOperation) as e:
            flash(f"Invalid amount: {str(e)}", "error")
            current_app.logger.warning(f"Invalid amount: {str(e)}")
            return redirect(request.url)
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding expense: {str(e)}", "error")
            current_app.logger.error(f"Error adding expense: {str(e)}")
            return redirect(request.url)

    return render_template("machinery/expense_add.html", machine=machine)


@machinery_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_machinery(id):
    machinery = Machinery.query.get_or_404(id)
    if request.method == "POST":
        new_name = request.form["name"]
        new_machine_type = request.form["type"]  # or whatever your form input is named
        last_service_input = request.form.get("last_service", "").strip()
        next_service_input = request.form.get("next_service", "").strip()

        # Update fields correctly
        machinery.name = new_name      # <-- Updated to a match model
        machinery.type = new_machine_type  # <-- Updated to a match model

        if last_service_input:
            try:
                machinery.last_service_date = datetime.strptime(last_service_input, "%Y-%m-%d")
            except ValueError:
                flash("Invalid Last Service date format.", "danger")
                current_app.logger.warning("Invalid Last Service date format.")
                return redirect(request.url)

        if next_service_input:
            try:
                machinery.next_service_due = datetime.strptime(next_service_input, "%Y-%m-%d")
            except ValueError:
                flash("Invalid Next Service Due date format.", "danger")
                current_app.logger.warning("Invalid Next Service Due date format.")
                return redirect(request.url)

        try:
            db.session.commit()
            flash("Machinery updated successfully!", "success")
            current_app.logger.info(f"Machinery updated: {machinery.id}")
            return redirect(url_for("machinery.list_machines"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating machinery: {str(e)}", "danger")
            current_app.logger.error(f"Error updating machinery: {str(e)}")

    return render_template("machinery/edit.html", machinery=machinery)



@machinery_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_machinery(id):
    machinery = Machinery.query.get_or_404(id)
    try:
        MachineryExpense.query.filter_by(machinery_id=id).delete()
        db.session.delete(machinery)
        db.session.commit()
        flash("Machinery and related expenses deleted successfully!", "success")
        current_app.logger.info(f"Machinery deleted: {machinery.id}")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting machinery: {str(e)}", "danger")
        current_app.logger.error(f"Error deleting machinery: {str(e)}")
    return redirect(url_for("machinery.list_machines"))


@machinery_bp.route("/<int:machinery_id>/expenses/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(machinery_id, expense_id):
    machinery = Machinery.query.get_or_404(machinery_id)
    try:
        expense = MachineryExpense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        # return redirect(url_for("machinery.list_expenses", id=machinery.id))
        return redirect(url_for("machinery.list_machines"))
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the expense.", "error")
        current_app.logger.error(f"Error deleting expense ID {expense_id} for machinery ID {machinery_id}: {e}")
        # return redirect(url_for("machinery.list_machines", id=machinery.id))
        return redirect(url_for("machinery.list_machines"))


@machinery_bp.route("/<int:machinery_id>/expenses/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit_expense(machinery_id, expense_id):
    machinery = Machinery.query.get_or_404(machinery_id)
    expense = MachineryExpense.query.get_or_404(expense_id)

    if expense.machinery_id != machinery.id:
        flash("Unauthorized action.", "error")
        current_app.logger.warning(f"Unauthorized edit attempt for expense ID {expense_id}")
        # return redirect(url_for("machinery.list_expenses", id=machinery.id))
        return redirect(url_for("machinery.list_machines"))

    if request.method == "POST":
        try:
            expense.category = request.form["category"]
            expense.amount = float(request.form["amount"])
            expense.description = request.form["description"]
            db.session.commit()
            flash("Expense updated successfully!", "success")
            current_app.logger.info(f"Expense updated: {expense.id}")
            # return redirect(url_for("machinery.list_expenses", id=machinery.id))
            return redirect(url_for("machinery.list_machines"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the expense.", "error")
            current_app.logger.error(f"Error updating expense ID {expense_id} for machinery ID {machinery_id}: {e}")
            return render_template("machinery/expense_edit.html", machinery=machinery, expense=expense)

    return render_template("machinery/expense_edit.html", machinery=machinery, expense=expense)


@machinery_bp.route("/expense/list/<int:id>")
@login_required
def list_expenses(id):
    machine = Machinery.query.get_or_404(id)
    expenses = MachineryExpense.query.filter_by(machinery_id=id).all()
    return render_template("machinery/list.html", machine=machine, expenses=expenses)


@machinery_bp.route("/expense/<int:id>")
@login_required
def view_expense(id):
    expense = MachineryExpense.query.get_or_404(id)
    return render_template("machinery/expense_view.html", expense=expense)