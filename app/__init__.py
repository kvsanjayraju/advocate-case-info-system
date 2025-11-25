from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'
login.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app import routes, models

    # Register blueprints or routes here
    # For MVP, we'll just import routes which will register themselves with the app context
    # But since routes.py will use `app`, we need to handle circular imports or use blueprints.
    # For a simple MVP structure, let's use the app object from routes if we define it there,
    # OR better, use `app.add_url_rule` or blueprints in routes.

    # However, the simplest way with the structure I proposed is to have routes import app from here,
    # which causes circular import if I create app here.
    # So I will use the "Application Factory" pattern but need to pass the app to routes.

    # Actually, for MVP simplicity, let's use the global app object pattern inside __init__.py
    # or use Blueprints. Blueprints are cleaner.

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.commands import send_reminders
    app.cli.add_command(send_reminders)

    return app
