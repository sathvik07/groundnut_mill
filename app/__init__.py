from flask import Flask
from flask_migrate import Migrate
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    # Import models to register with SQLAlchemy
    from . import models  # makes sure all models are imported

    # Blueprints can be registered here later
    from .routes import register_routes
    register_routes(app)

    return app
