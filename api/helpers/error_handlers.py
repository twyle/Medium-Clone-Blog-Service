# -*- coding: utf-8 -*-
"""This module declares the error handlers."""
from flask import jsonify

from .http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


def handle_resource_not_found(e):
    """Handle all resource not found errors."""
    return jsonify({"error": str(e)}), HTTP_404_NOT_FOUND


def handle_method_not_allowed(e):
    """Handle all method not allowed errors."""
    return jsonify({"error": str(e)}), HTTP_405_METHOD_NOT_ALLOWED


def handle_internal_server_error(e):
    """Handle all internal server errors."""
    return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


def register_error_handlers(app):
    """Register the error handlers."""
    app.register_error_handler(HTTP_404_NOT_FOUND, handle_resource_not_found)
    app.register_error_handler(HTTP_405_METHOD_NOT_ALLOWED, handle_method_not_allowed)
    app.register_error_handler(
        HTTP_500_INTERNAL_SERVER_ERROR, handle_internal_server_error
    )
