from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models
from .supplier import Supplier
from .raw_stock import RawStock
from .processed_stock import ProcessedStock
from .debt import Debt
from .vehicle import Vehicle
from .vehicle_expense import VehicleExpense
from .machinery import Machinery
from .machinery_expense import MachineryExpense
from .service_schedule import ServiceSchedule
from .distributor import Distributor
from .sale import Sale
