from flask import Flask, jsonify
from .config import Config


def create_app(config_name='default'):
    """Create the Flask app instance."""
    app = Flask(__name__)
    
    app.config.from_object(Config[config_name])
    
    @app.route('/')
    def health_check():
        return jsonify({'success': 'hello from flask'}), 200
    
    app.shell_context_processor({'app': app})
    
    return app