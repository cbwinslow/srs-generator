# Backend Configuration

class Config:
    SECRET_KEY = 'dev'
    OPENROUTER_API_KEY = None
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
