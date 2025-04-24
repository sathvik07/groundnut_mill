from flask import Blueprint

def register_routes(app):
    from .supplier_routes import supplier_bp
    app.register_blueprint(supplier_bp, url_prefix="/suppliers")

    from .raw_stock_routes import raw_stock_bp
    app.register_blueprint(raw_stock_bp, url_prefix="/raw_stock")

    from .debt_routes import debt_bp
    app.register_blueprint(debt_bp, url_prefix="/debts")

    from .vehicle_routes import vehicle_bp
    app.register_blueprint(vehicle_bp, url_prefix="/vehicles")

    from .machinery_routes import machinery_bp
    app.register_blueprint(machinery_bp, url_prefix="/machineries")

    from .dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    from .processed_stock_routes import processed_stock_bp
    app.register_blueprint(processed_stock_bp)
