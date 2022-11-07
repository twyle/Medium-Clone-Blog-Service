from flask import Flask, jsonify
from .config import Config
from .helpers import register_extensions, register_blueprints
from .extensions import db


def create_app(config_name='default'):
    """Create the Flask app instance."""
    app = Flask(__name__)
    
    app.config.from_object(Config[config_name])
    register_extensions(app)
    register_blueprints(app)
    
    @app.route('/')
    def health_check():
        return jsonify({'success': 'hello from flask'}), 200
    
    app.shell_context_processor({'app': app, 'db': db})
    
    return app