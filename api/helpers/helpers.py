from ..extensions import (
    db,
    ma,
    migrate,
    cors,
    swagger
)
from flasgger import LazyJSONEncoder
from ..author import author


def register_extensions(app):
    """Register the app extensions."""
    app.json_encoder = LazyJSONEncoder
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    swagger.init_app(app)
    

def register_blueprints(app):
    app.register_blueprint(author, url_prefix='/author')
    