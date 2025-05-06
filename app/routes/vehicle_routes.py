from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
import pytz
from app.models import db, Vehicle, VehicleExpense
from datetime import datetime

vehicle_bp = Blueprint("vehicle", __name__)

@vehicle_bp.route("/")
@login_required
def list_vehicles():
    """List all vehicles."""
    try:
        vehicles = Vehicle.query.all()
        return render_template("vehicle/list.html", vehicles=vehicles)
    except Exception as e:
        flash("An error occurred while retrieving vehicles.", "error")
        current_app.logger.error(f"Error retrieving vehicles: {e}")
        return render_template("vehicle/list.html", vehicles=[])

@vehicle_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_vehicle():
    if request.method == "POST":
        number = request.form.get('vehicle_number')
        name = request.form["name"]
        notes = request.form["notes"]

        if not number or not name:
            flash("Vehicle number and name are required.", "error")
            return render_template("vehicle/add.html")

        vehicle = Vehicle(number_plate=number, name=name, description=notes)
        try:
            db.session.add(vehicle)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while adding the vehicle.", "error")
            current_app.logger.error(f"Error adding vehicle: {e}")
            return render_template("vehicle/add.html")

        return redirect(url_for("vehicle.list_vehicles"))

    return render_template("vehicle/add.html")

@vehicle_bp.route('/vehicles/<int:vehicle_id>/edit', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if request.method == 'POST':
        vehicle.name = request.form['name']
        vehicle.number_plate = request.form['number_plate']
        vehicle.description = request.form['description']
        db.session.commit()
        # flash('Vehicle updated successfully.', 'success')
        return redirect(url_for('vehicle.list_vehicles'))
    return render_template('vehicle/edit_vehicles_info.html', vehicle=vehicle)

@vehicle_bp.route('/vehicles/<int:vehicle_id>/delete', methods=['POST'])
@login_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    # Optional: Also delete associated expenses if needed
    VehicleExpense.query.filter_by(vehicle_id=vehicle.id).delete()

    db.session.delete(vehicle)
    db.session.commit()

    return redirect(url_for('vehicle.list_vehicles'))



@vehicle_bp.route("/<int:vehicle_id>/expenses", methods=["GET", "POST"])
@login_required
def add_expense(vehicle_id):
    """Add an expense for a specific vehicle."""
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == "POST":
        category = request.form.get("category")
        amount = request.form.get("amount")
        description = request.form.get("description")

        if not category or not amount or not description:
            flash("All fields are required.", "error")
            current_app.logger.warning("Expense form submission failed: Missing fields.")
            return render_template("vehicle/expense_add.html", vehicle=vehicle)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            flash("Invalid amount. Please enter a positive number.", "error")
            current_app.logger.warning("Invalid amount entered for expense.")
            return render_template("vehicle/expense_add.html", vehicle=vehicle)

        tz = pytz.timezone("UTC")  # Replace "UTC" with your desired timezone
        date = datetime.now(tz)

        expense = VehicleExpense(
            vehicle_id=vehicle.id,
            category=category,
            amount=amount,
            notes=description,
            date=date
        )
        try:
            db.session.add(expense)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while adding the expense.", "error")
            current_app.logger.error(f"Error adding expense for vehicle ID {vehicle_id}: {e}")
            return render_template("vehicle/expense_add.html", vehicle=vehicle)

        return redirect(url_for("vehicle.view_vehicle", vehicle_id=vehicle.id))

    return render_template("vehicle/expense_add.html", vehicle=vehicle)

@vehicle_bp.route("/edit/<int:vehicle_id>", methods=["GET", "POST"])
@login_required
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == "POST":
        try:
            vehicle.number_plate = request.form["vehicle_number"]
            vehicle.name = request.form["name"]
            vehicle.description = request.form["notes"]
            db.session.commit()
            return redirect(url_for("vehicle.list_vehicles"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the vehicle.", "error")
            current_app.logger.error(f"Error updating vehicle ID {vehicle_id}: {e}")
            return render_template("vehicle/edit.html", vehicle=vehicle)

    return render_template("vehicle/edit.html", vehicle=vehicle)


@vehicle_bp.route("/delete/<int:vehicle_id>", methods=["POST"])
@login_required
def delete_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        db.session.delete(vehicle)
        db.session.commit()
        return redirect(url_for("vehicle.list_vehicles"))
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the vehicle.", "error")
        current_app.logger.error(f"Error deleting vehicle ID {vehicle_id}: {e}")
        return redirect(url_for("vehicle.list_vehicles"))


@vehicle_bp.route("/<int:vehicle_id>/expenses/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(vehicle_id, expense_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    try:
        expense = VehicleExpense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        return redirect(url_for("vehicle.add_expense", vehicle_id=vehicle.id))
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the expense.", "error")
        current_app.logger.error(f"Error deleting expense ID {expense_id} for vehicle ID {vehicle_id}: {e}")
        return redirect(url_for("vehicle.add_expense", vehicle_id=vehicle.id))


@vehicle_bp.route("/<int:vehicle_id>/expenses/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit_expense(vehicle_id, expense_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    expense = VehicleExpense.query.get_or_404(expense_id)

    if request.method == "POST":
        try:
            expense.category = request.form["category"]
            expense.amount = float(request.form["amount"])
            expense.notes = request.form["description"]
            db.session.commit()
            return redirect(url_for("vehicle.add_expense", vehicle_id=vehicle.id))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the expense.", "error")
            current_app.logger.error(f"Error updating expense ID {expense_id} for vehicle ID {vehicle_id}: {e}")
            return render_template("vehicle/expense_edit.html", vehicle=vehicle, expense=expense)


    return render_template("vehicle/expense_edit.html", vehicle=vehicle, expense=expense)


@vehicle_bp.route("/<int:vehicle_id>/expenses")
@login_required
def list_expenses(vehicle_id):
    try:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        expenses = VehicleExpense.query.filter_by(vehicle_id=vehicle.id).all()
        return render_template("vehicle/expense_list.html", vehicle=vehicle, expenses=expenses)
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while retrieving expenses.", "error")
        current_app.logger.error(f"Error retrieving expenses for vehicle ID {vehicle_id}: {e}")
        return redirect(url_for("vehicle.view_vehicle", vehicle_id=vehicle.id))

@vehicle_bp.route("/<int:vehicle_id>/expenses/<int:expense_id>")
@login_required
def view_expense(vehicle_id, expense_id):
    """View a specific vehicle expense."""
    try:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        expense = VehicleExpense.query.get_or_404(expense_id)
        return render_template("vehicle/expense_view.html", vehicle=vehicle, expense=expense)
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while retrieving the expense.", "error")
        current_app.logger.error(f"Error retrieving expense ID {expense_id} for vehicle ID {vehicle_id}: {e}")
        return redirect(url_for("vehicle.list_vehicles"))


@vehicle_bp.route("/<int:vehicle_id>")
@login_required
def view_vehicle(vehicle_id):
    """View a specific vehicle and its expenses."""
    try:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        expenses = VehicleExpense.query.filter_by(vehicle_id=vehicle.id).all()
        return render_template("vehicle/view.html", vehicle=vehicle, expenses=expenses)
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while retrieving the vehicle.", "error")
        current_app.logger.error(f"Error retrieving vehicle ID {vehicle_id}: {e}")
        return redirect(url_for("vehicle.list_vehicles"))



