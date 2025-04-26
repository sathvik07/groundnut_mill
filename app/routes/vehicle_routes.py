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
