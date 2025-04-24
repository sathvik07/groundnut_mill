from app.models import db, Supplier, RawStock, ProcessedStock, Distributor, Sale, Vehicle, VehicleExpense, Debt, Machinery, MachineryExpense, ServiceSchedule
from datetime import datetime

def seed_data():
    # Example Suppliers
    supplier1 = Supplier(name="Ramesh", type="Farmer", contact="9876543210")
    supplier2 = Supplier(name="Suresh", type="Broker", contact="9876501234")
    db.session.add_all([supplier1, supplier2])
    db.session.commit()

    # Raw Stock
    raw1 = RawStock(supplier_id=supplier1.id, weight_kg=500, gram=10000, date=datetime.utcnow())
    raw2 = RawStock(supplier_id=supplier2.id, weight_kg=300, gram=5000, date=datetime.utcnow())
    db.session.add_all([raw1, raw2])
    db.session.commit()

    # Processed Stock
    processed1 = ProcessedStock(raw_stock_id=raw1.id, expected_weight=450)
    db.session.add(processed1)
    db.session.commit()

    # Distributor
    dist1 = Distributor(name="ABC Traders", contact="9123456789", address="Market Street")
    db.session.add(dist1)
    db.session.commit()

    # Sale
    sale1 = Sale(distributor_id=dist1.id, processed_stock_id=processed1.id,
                 quantity_sold=100, price_per_kg=70, total_price=7000)
    db.session.add(sale1)
    db.session.commit()

    # Vehicle
    vehicle1 = Vehicle(name="Transporter", number_plate="TN01AB1234", description="Tata Ace")
    db.session.add(vehicle1)
    db.session.commit()

    # Vehicle Expense
    expense1 = VehicleExpense(vehicle_id=vehicle1.id, category="Fuel", amount=1000, date=datetime.utcnow(), notes="Diesel")
    db.session.add(expense1)
    db.session.commit()

    # Machinery
    mach1 = Machinery(name="Grinder", type="Type-A")
    db.session.add(mach1)
    db.session.commit()

    # Machinery Expense
    mech_exp = MachineryExpense(machinery_id=mach1.id, category="Repair", amount=500, date=datetime.utcnow(), description="Replaced belt")
    db.session.add(mech_exp)

    # Service Schedule
    service = ServiceSchedule(machinery_id=mach1.id, service_date=datetime.utcnow(), notes="Quarterly maintenance")
    db.session.add(service)

    # Debt
    debt = Debt(supplier_id=supplier1.id, amount=10000, total_cost=12000, goods_id=raw1.id, notes="Advance payment")
    db.session.add(debt)

    db.session.commit()
