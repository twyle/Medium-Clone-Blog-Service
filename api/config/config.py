from dotenv import load_dotenv
import os

load_dotenv()


class BaseConfig:
    """Base configuration."""
    DEBUG = True
    TESTING = False
    
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

    db_conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = db_conn_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(BaseConfig):
    """Development confuguration."""
    EMAIL_MAX_LENGTH = int(os.getenv("EMAIL_MAX_LENGTH", "64"))
    EMAIL_MIN_LENGTH = int(os.getenv("EMAIL_MIN_LENGTH", "8"))

    NAME_MAX_LENGTH = int(os.getenv("NAME_MAX_LENGTH", "20"))
    NAME_MIN_LENGTH = int(os.getenv("NAME_MIN_LENGTH", "2"))
    
    TITLE_MAX_LENGTH = int(os.getenv("TITLE_MAX_LENGTH", "100"))
    TITLE_MIN_LENGTH = int(os.getenv("TITLE_MIN_LENGTH", "2"))


Config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,
    'default': DevelopmentConfig
}