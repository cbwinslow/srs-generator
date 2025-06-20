from flask import Flask
from .config import DevelopmentConfig
from .logging import setup_logging

def create_app(config_object=DevelopmentConfig):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Set up logging
    setup_logging(app)
    
    # Register blueprints
    from .ai import bp as ai_bp
    app.register_blueprint(ai_bp)
    
    app.logger.info(f"Application configured with {config_object.__name__}")
    return app
