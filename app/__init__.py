from flask import Flask
from config import Config
from app.extensions import db, migrate, mail, limiter
from flasgger import Swagger

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    limiter.init_app(app)
    
    # Swagger Configuration
    app.config['SWAGGER'] = {
        'title': 'Secure Task Orchestrator API',
        'uiversion': 3
    }
    swagger = Swagger(app)

    # Register Blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    # Register generic error handlers (global)
    from app.middleware.error_handlers import register_error_handlers
    register_error_handlers(app)

    return app
