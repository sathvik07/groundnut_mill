from flask import Flask, current_app
from flask_login import current_user
from flask_migrate import Migrate
from .extensions import login_manager
from .models import db
from flask_caching import Cache
from app.utils.logger import setup_logger


cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    with app.app_context():
        print(current_app.static_folder)

    # Setup logger
    logger = setup_logger('flask-app')
    app.logger.handlers = logger.handlers  # Use handlers from the custom logger
    app.logger.setLevel(logger.level)

    logger.info("Starting Flask application...")
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    cache.init_app(app)

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

    # Log unhandled exceptions
    @app.errorhandler(Exception)
    def handle_exception(e):
        current_app.logger.error(f"Unhandled exception: {e}", exc_info=True)
        return "An internal error occurred.", 500

    return app
