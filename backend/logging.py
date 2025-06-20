import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask


def setup_logging(app):
    """Configure logging for the application."""
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Configure file handler
    file_handler = RotatingFileHandler(
        "logs/srs_generator.log", maxBytes=10240000, backupCount=10  # 10MB
    )
    file_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )
    file_handler.setLevel(logging.INFO)

    # Configure stream handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    console_handler.setLevel(logging.INFO)

    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

    # Log application startup
    app.logger.info("SRS Generator starting up...")
