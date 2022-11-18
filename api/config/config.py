from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()


class BaseConfig:
    """Base configuration."""
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

    db_conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = db_conn_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    EMAIL_MAX_LENGTH = int(os.getenv("EMAIL_MAX_LENGTH", "64"))
    EMAIL_MIN_LENGTH = int(os.getenv("EMAIL_MIN_LENGTH", "8"))

    NAME_MAX_LENGTH = int(os.getenv("NAME_MAX_LENGTH", "20"))
    NAME_MIN_LENGTH = int(os.getenv("NAME_MIN_LENGTH", "2"))
    
    TITLE_MAX_LENGTH = int(os.getenv("TITLE_MAX_LENGTH", "100"))
    TITLE_MIN_LENGTH = int(os.getenv("TITLE_MIN_LENGTH", "2"))
    
    S3_BUCKET = os.environ["S3_BUCKET"]
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_ACCESS_SECRET = os.environ["AWS_ACCESS_SECRET"]
    AWS_REGION = os.environ['AWS_REGION']
    S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = BASE_DIR
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    
    JWT_SECRET_KEY = "super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "24"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "7"))
    )
    
    
class DevelopmentConfig(BaseConfig):
    """Development confuguration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

    db_conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = db_conn_string
    
    EMAIL_MAX_LENGTH = int(os.getenv("EMAIL_MAX_LENGTH", "64"))
    EMAIL_MIN_LENGTH = int(os.getenv("EMAIL_MIN_LENGTH", "8"))

    NAME_MAX_LENGTH = int(os.getenv("NAME_MAX_LENGTH", "20"))
    NAME_MIN_LENGTH = int(os.getenv("NAME_MIN_LENGTH", "2"))
    
    TITLE_MAX_LENGTH = int(os.getenv("TITLE_MAX_LENGTH", "100"))
    TITLE_MIN_LENGTH = int(os.getenv("TITLE_MIN_LENGTH", "2"))
    
    S3_BUCKET = os.environ["S3_BUCKET"]
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_ACCESS_SECRET = os.environ["AWS_ACCESS_SECRET"]
    AWS_REGION = os.environ['AWS_REGION']
    S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = BASE_DIR
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    
    JWT_SECRET_KEY = "super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "24"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "7"))
    )
    
    
class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')

    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

    db_conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = db_conn_string
    
    EMAIL_MAX_LENGTH = int(os.getenv("EMAIL_MAX_LENGTH", "64"))
    EMAIL_MIN_LENGTH = int(os.getenv("EMAIL_MIN_LENGTH", "8"))

    NAME_MAX_LENGTH = int(os.getenv("NAME_MAX_LENGTH", "20"))
    NAME_MIN_LENGTH = int(os.getenv("NAME_MIN_LENGTH", "2"))
    
    TITLE_MAX_LENGTH = int(os.getenv("TITLE_MAX_LENGTH", "100"))
    TITLE_MIN_LENGTH = int(os.getenv("TITLE_MIN_LENGTH", "2"))
    
    S3_BUCKET = os.environ["S3_BUCKET"]
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_ACCESS_SECRET = os.environ["AWS_ACCESS_SECRET"]
    AWS_REGION = os.environ['AWS_REGION']
    S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = BASE_DIR
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    
    JWT_SECRET_KEY = "super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "24"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "7"))
    )
    

class ProductionConfig(BaseConfig):
    """Production configuration."""
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

    db_conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = db_conn_string
    
    EMAIL_MAX_LENGTH = int(os.getenv("EMAIL_MAX_LENGTH", "64"))
    EMAIL_MIN_LENGTH = int(os.getenv("EMAIL_MIN_LENGTH", "8"))

    NAME_MAX_LENGTH = int(os.getenv("NAME_MAX_LENGTH", "20"))
    NAME_MIN_LENGTH = int(os.getenv("NAME_MIN_LENGTH", "2"))
    
    TITLE_MAX_LENGTH = int(os.getenv("TITLE_MAX_LENGTH", "100"))
    TITLE_MIN_LENGTH = int(os.getenv("TITLE_MIN_LENGTH", "2"))
    
    S3_BUCKET = os.environ["S3_BUCKET"]
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_ACCESS_SECRET = os.environ["AWS_ACCESS_SECRET"]
    AWS_REGION = os.environ['AWS_REGION']
    S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = BASE_DIR
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    
    JWT_SECRET_KEY = "super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "24"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "7"))
    )


Config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}