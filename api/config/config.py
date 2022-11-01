from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration."""
    DEBUG = True
    TESTING = False
    
class DevelopmentConfig(BaseConfig):
    """Development confuguration."""


Config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,
    'default': DevelopmentConfig
}