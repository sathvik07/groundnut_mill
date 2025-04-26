from flask import Flask
from flask_login import current_user
from flask_migrate import Migrate
from .extensions import login_manager
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # Import models to register with SQLAlchemy
    from . import models  # makes sure all models are imported

    # Blueprints can be registered here later
    from .routes import register_routes
    register_routes(app)

    return app
