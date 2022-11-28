# -*- coding: utf-8 -*-
"""This module creates the flask application.

It also:
1. Initializes the extensions.
2. Registers the error handlers.
3. Registers the blueprints.
4. Registers the request loggers.
"""
import os
import sys

from flask import Flask, jsonify, request

from .article.controller.helpers import handle_delete_image, handle_get_image
from .config import Config
from .config.logger import app_logger
from .extensions import db
from .helpers import check_configuration, register_blueprints, register_extensions
from .helpers.error_handlers import register_error_handlers
from .helpers.hooks import get_exception, get_response, log_get_request, log_post_request
from .helpers.http_status_codes import HTTP_200_OK


def create_app(config_name=os.environ.get("FLASK_ENV", "development")):
    """Create the Flask app instance.

    This function creates the Flask app instance, registers
    the error handlers and the blueprints.

    Parameters
    ----------
    config_name: str
        The name of the confguration to use. Can be development
        testing or production.

    Raises
    ------
    Valuerror
        If the database is not connected
        If the ELK cluster is not connected

    Returns
    -------
    app: flask.Flask
        The flask app instance
    """
    app = Flask(__name__)

    app.config.from_object(Config[config_name])
    try:
        check_configuration()
    except ValueError as e:
        app_logger.critical(str(e))
        sys.exit(1)

    register_error_handlers(app)
    app_logger.info("Registered the error handlers!")

    @app.before_first_request
    def application_startup():
        """Log the beginning of the application."""
        app_logger.info("Web app is up!")

    @app.before_request
    def log_request():
        """Log the data held in the request."""
        if request.method in {"POST", "PUT"}:
            log_post_request()
        elif request.method in {"GET", "DELETE"}:
            log_get_request()

    @app.after_request
    def log_response(response):
        """Log the data held in the response."""
        try:
            get_response(response)
        except Exception:
            pass
        finally:
            return response

    @app.teardown_request
    def log_exception(exc):
        """Log the data held in the exception."""
        get_exception(exc)

    register_extensions(app)
    app_logger.info("Registered the extensions!")
    register_blueprints(app)
    app_logger.info("Registered the blueprints!")

    @app.route("/")
    def health_check():
        """Check if the application is running."""
        return jsonify({"success": "hello from flask"}), HTTP_200_OK

    @app.route("/image")
    def get_image():
        """Fetch an image uploaded and stored in the server.

        This route is accessed by the Lambda function in
        order to upload the image stored locally to s3.
        """
        return handle_get_image(request.args.get("filename"))

    @app.route("/delete")
    def delete_image():
        """Delete an image after being uploaded to s3.

        This route is accessed by a lambda function to
        trigger the deletion of animage after it's uploaded
        to s3.
        """
        return handle_delete_image(request.args.get("filename"))

    app.shell_context_processor({"app": app, "db": db})

    return app
