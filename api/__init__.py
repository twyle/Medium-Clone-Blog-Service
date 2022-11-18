from flask import Flask, jsonify
from .config import Config
from .helpers import register_extensions, register_blueprints, check_configuration
from .extensions import db
import sys
from flask import request
from .helpers.hooks import log_get_request, log_post_request, get_response, get_exception
from .config.logger import app_logger
from .helpers.error_handlers import register_error_handlers
from .helpers.http_status_codes import HTTP_200_OK
import os

def create_app(config_name=os.environ.get('FLASK_ENV', 'development')):
    """Create the Flask app instance."""
    app = Flask(__name__)
    
    app.config.from_object(Config[config_name])
    try:
        check_configuration()
    except Exception as e:
        app_logger.critical(str(e))
        sys.exit(1)
        
    register_error_handlers(app)
    app_logger.info('Registered the error handlers!')
    
        
    # @app.before_first_request
    # def application_startup():
    #     """Log the beginning of the application."""
    #     app_logger.info('Web app is up!')
        
    # @app.before_request
    # def log_request():
    #     """Log the data held in the request"""
    #     if request.method in ['POST', 'PUT']:
    #         log_post_request()
    #     elif request.method in ['GET', 'DELETE']:
    #         log_get_request()
            
    # @app.after_request
    # def log_response(response):
    #     try:
    #         get_response(response)
    #     except Exception:
    #         pass
    #     finally:
    #         return response
    
    # @app.teardown_request
    # def log_exception(exc):
    #     get_exception(exc)
        
    register_extensions(app)
    app_logger.info('Registered the extensions!')
    register_blueprints(app)
    app_logger.info('Registered the blueprints!')
    
    @app.route('/')
    def health_check():
        return jsonify({'success': 'hello from flask'}), HTTP_200_OK
    
    app.shell_context_processor({'app': app, 'db': db})
    
    return app