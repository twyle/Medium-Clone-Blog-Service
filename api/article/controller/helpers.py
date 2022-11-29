# -*- coding: utf-8 -*-
"""This module declares helper methods used by the article.py
module.

Has the following functions:
1. allowed_file():
    Checks if the given file can be uploaded to the server
    based on the file's extension.
2. send_notification():
    Sends the filename and whether is is to be created or
    deleted to an sns queue.
3. upload_image():
    Saves the uploaded image to the server and sends a notification
    to the sns queue.
"""
import os

from flask import Response, current_app, jsonify, send_file


def handle_get_image(filename: str) -> Response:
    """Loads the image.

    This route is used by the lambda function to upload
    the image.

    Parameters
    ----------
    filename: str
        The name of the file to be uploaded.

    Returns
    ------
    file:
        The image to be stored in s3
    """
    try:
        file = get_image(filename)
    except (ValueError) as e:
        return jsonify({"error": str(e)})
    else:
        return file


def get_image(filename: str) -> Response:
    """Load a stored image.

    Parameters
    ----------
    filename: str
        The name of the file to be loaded.

    Returns
    -------
    Image:
        The loaded image.
    """
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    return send_file(file_path)
