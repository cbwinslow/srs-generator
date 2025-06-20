from flask import Flask
from .config import DevelopmentConfig

def create_app(config_object=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    from .ai import bp as ai_bp
    app.register_blueprint(ai_bp)
    
    return app
