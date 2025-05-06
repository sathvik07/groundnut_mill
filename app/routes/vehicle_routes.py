from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app.models import db, Vehicle, VehicleExpense
from datetime import datetime

vehicle_bp = Blueprint("vehicle", __name__)

@vehicle_bp.route("/")
@login_required
def list_vehicles():
    vehicles = Vehicle.query.all()
    return render_template("vehicle/list.html", vehicles=vehicles)

@vehicle_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_vehicle():
    if request.method == "POST":
        number = request.form.get('vehicle_number')
        # type_ = request.form["type"]
        name = request.form["name"]
        notes = request.form["notes"]
        vehicle = Vehicle(number_plate=number, name=name, description=notes)
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for("vehicle.list_vehicles"))

    return render_template("vehicle/add.html")



@vehicle_bp.route("/<int:vehicle_id>/expenses", methods=["GET", "POST"])
@login_required
def add_expense(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        description = request.form["description"]
        date = datetime.now()

        expense = VehicleExpense(
            vehicle_id=vehicle.id,
            category=category,
            amount=amount,
            notes=description,
            date=date
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for("vehicle.list_vehicles"))

    return render_template("vehicle/expense_add.html", vehicle=vehicle)


@vehicle_bp.route("/edit/<int:vehicle_id>", methods=["GET", "POST"])
@login_required
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == "POST":
        vehicle.number_plate = request.form["number_plate"]
        vehicle.name = request.form["name"]
        vehicle.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("vehicle.list_vehicles"))

    return render_template("vehicle/edit.html", vehicle=vehicle)


@vehicle_bp.route("/delete/<int:vehicle_id>", methods=["POST"])
@login_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for("vehicle.list_vehicles"))

@vehicle_bp.route("/<int:vehicle_id>/expenses/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(vehicle_id, expense_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    expense = VehicleExpense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("vehicle.list_vehicles", vehicle_id=vehicle.id))


@vehicle_bp.route("/<int:vehicle_id>/expenses/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit_expense(vehicle_id, expense_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    expense = VehicleExpense.query.get_or_404(expense_id)

    if request.method == "POST":
        expense.category = request.form["category"]
        expense.amount = float(request.form["amount"])
        expense.notes = request.form["description"]
        db.session.commit()
        return redirect(url_for("vehicle.list_vehicles", vehicle_id=vehicle.id))

    return render_template("vehicle/expense_edit.html", vehicle=vehicle, expense=expense)


@vehicle_bp.route("/<int:vehicle_id>/expenses")
@login_required
def list_expenses(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    expenses = VehicleExpense.query.filter_by(vehicle_id=vehicle.id).all()
    return render_template("vehicle/expense_list.html", vehicle=vehicle, expenses=expenses)

@vehicle_bp.route("/<int:vehicle_id>/expenses/<int:expense_id>")
@login_required
def view_expense(vehicle_id, expense_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    expense = VehicleExpense.query.get_or_404(expense_id)
    return render_template("vehicle/expense_view.html", vehicle=vehicle, expense=expense)


@vehicle_bp.route("/<int:vehicle_id>")
@login_required
def view_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    expenses = VehicleExpense.query.filter_by(vehicle_id=vehicle.id).all()
    return render_template("vehicle/view.html", vehicle=vehicle, expenses=expenses)


