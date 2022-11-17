from flask import Flask, jsonify
from .config import Config, app_logger
from .helpers import register_extensions, register_blueprints, check_configuration
from .extensions import db
import sys
from flask import request
from .helpers.hooks import log_get_request, log_post_request, get_response, get_exception


def create_app(config_name='default'):
    """Create the Flask app instance."""
    app = Flask(__name__)
    
    app.config.from_object(Config[config_name])
    try:
        check_configuration()
    except Exception as e:
        print('Exiting')
        sys.exit(1)
    
        
    @app.before_first_request
    def application_startup():
        """Log the beginning of the application."""
        app_logger.info('Web app is up!')
        
    @app.before_request
    def log_request():
        """Log the data held in the request"""
        if request.method in ['POST', 'PUT']:
            log_post_request()
        elif request.method in ['GET', 'DELETE']:
            log_get_request()
            
    @app.after_request
    def log_response(response):
        get_response(response)
        return response
    
    @app.teardown_request
    def log_exception(exc):
        get_exception(exc)
        
    register_extensions(app)
    app_logger.info('Registered the extensions!')
    register_blueprints(app)
    app_logger.info('Registered the blueprints!')
    
    @app.route('/')
    def health_check():
        return jsonify({'success': 'hello from flask'}), 200
    
    app.shell_context_processor({'app': app, 'db': db})
    
    return app