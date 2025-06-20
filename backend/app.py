from flask import Flask, request
from .config import DevelopmentConfig
from .logging import setup_logging
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

def create_app(config_object=DevelopmentConfig):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Set up logging
    setup_logging(app)
    
    # Register blueprints
    from .ai import bp as ai_bp
    from .monitoring import bp as monitoring_bp
    app.register_blueprint(ai_bp)
    app.register_blueprint(monitoring_bp)
    
    # Add Prometheus metrics WSGI middleware
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        "/metrics": make_wsgi_app()
    })
    
    # Request tracking
    @app.before_request
    def before_request():
        # Skip metrics endpoint
        if request.path == "/metrics":
            return
        request.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        # Skip metrics endpoint
        if request.path == "/metrics":
            return response
            
        # Record metrics
        from .monitoring import record_request_metric, stop_request_timer
        record_request_metric(response.status_code)
        if hasattr(request, "start_time"):
            stop_request_timer(request.start_time, request.endpoint)
            
        return response
    
    app.logger.info(f"Application configured with {config_object.__name__}")
    return app
