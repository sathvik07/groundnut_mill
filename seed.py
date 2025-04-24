from app import create_app
from app.models import db, Supplier, RawStock, ProcessedStock, Distributor, Sale, Debt, Machinery, MachineryExpense, ServiceSchedule, Vehicle, VehicleExpense
from datetime import datetime

app = create_app()

with app.app_context():
    # Create all tables if they don't exist
    db.create_all()

    # Supplier
    supplier = Supplier(name="Ramu", type="Farmer", contact="9876543210")
    db.session.add(supplier)
    db.session.commit()

    # Raw Stock
    raw_stock = RawStock(supplier_id=supplier.id, weight_kg=1000, gram=50, date=datetime.now())
    db.session.add(raw_stock)
    db.session.commit()

    # Processed Stock
    processed_stock = ProcessedStock(raw_stock_id=raw_stock.id, expected_weight=850)
    db.session.add(processed_stock)
    db.session.commit()

    # Distributor
    distributor = Distributor(name="Kiran Traders", contact="1234567890", address="Guntur")
    db.session.add(distributor)
    db.session.commit()

    # Sale
    sale = Sale(distributor_id=distributor.id, processed_stock_id=processed_stock.id, quantity_sold=500, price_per_kg=120, total_price=60000)
    db.session.add(sale)
    db.session.commit()

    # Debt
    debt = Debt(supplier_id=supplier.id, amount=20000, total_cost=22000, goods_id=raw_stock.id, notes="Advance payment")
    db.session.add(debt)
    db.session.commit()

    # Machinery
    machine = Machinery(name="Grinder 3000", type="Grinder")
    db.session.add(machine)
    db.session.commit()

    # Machinery Expense
    mach_exp = MachineryExpense(machinery_id=machine.id, category="Repair", amount=5000, date=datetime.now(), description="Fixed broken belt")
    db.session.add(mach_exp)
    db.session.commit()

    # Service Schedule
    service = ServiceSchedule(machinery_id=machine.id, service_date=datetime.now(), notes="Monthly maintenance")
    db.session.add(service)
    db.session.commit()

    # Vehicle
    vehicle = Vehicle(name="Tata Ace", number_plate="KA34AB1234", description="Used for local transport")
    db.session.add(vehicle)
    db.session.commit()

    # Vehicle Expense
    vehicle_exp = VehicleExpense(vehicle_id=vehicle.id, category="Fuel", amount=3000, date=datetime.now(), notes="Refueling")
    db.session.add(vehicle_exp)
    db.session.commit()

    print("✅ Sample data added to all tables!")
