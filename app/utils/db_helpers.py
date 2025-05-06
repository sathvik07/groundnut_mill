# app/utils/db_helpers.py
from app.models import Vehicle, VehicleExpense

def get_vehicle_or_404(vehicle_id):
    """Fetch a vehicle by ID or return a 404 error."""
    return Vehicle.query.get_or_404(vehicle_id)

def get_expense_or_404(expense_id):
    """Fetch a vehicle expense by ID or return a 404 error."""
    return VehicleExpense.query.get_or_404(expense_id)

def get_expenses_by_vehicle(vehicle_id):
    """Fetch all expenses for a specific vehicle."""
    return VehicleExpense.query.filter_by(vehicle_id=vehicle_id).all()