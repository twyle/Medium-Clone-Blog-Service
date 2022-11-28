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
import json
import os

from flask import current_app, jsonify, send_file
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ...extensions import sqs_client


def allowed_file(filename: str) -> bool:
    """Check if the file is allowed.

    Parameters
    ----------
    filename: str
        The name of the uploaded file with its extension

    Raises
    ------
    TypeError:
        If the filename is not a string or has not extension
    ValuError:
        If the filename is empty

    returns
    -------
    bool:
        True if file is allowed else False
    """
    if not filename:
        raise ValueError("The filename must be provided!")
    if not isinstance(filename, str):
        raise TypeError("The filename has to be a string.")
    if "." not in filename:
        raise TypeError("The file lacks an extension")
    allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def send_notification(filename: str, action: str):
    """Send notification to sqs.

    Parameters
    ----------
    filename: str
        The name of the file
    action: str
        What action to take i.e create or delete
        create results in lambda function uploading the file
        wheres delete results in deletion of file from s3.
    Returns
    -------
    bool:
        True if notification was sent else False.
    """
    queue_url = os.environ["QUEUE_URL"]
    message = {action: filename}
    response = sqs_client.send_message(
        QueueUrl=queue_url, MessageBody=json.dumps(message)
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return True
    return False


def save_image(file: FileStorage) -> bool:
    """Save a file in the server.

    Parameters
    ----------
    file: werkzeug.FileStorage
        The uploaded file and its metadata.

    Raises
    ------
    Exception:
        When the image cannot be saved

    return
    ------
    bool:
        Whether or not file was successfully stored.
    """
    try:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    except Exception as e:
        raise e
    else:
        return True


def upload_image(file):
    """Upload image to S3."""
    if not file:
        raise ValueError("The file has to be provided!")
    if file.filename == "":
        raise ValueError("The file has to be provided!")
    if not allowed_file(file.filename):
        raise TypeError("That file type is not allowed!")
    save_image(file)
    if send_notification(file.filename, "create"):
        profile_pic = f"{current_app.config['S3_LOCATION']}{file.filename}"
        return profile_pic
    return ""


def handle_get_image(filename: str):
    """Loads the image."""
    try:
        file = get_image(filename)
    except (ValueError) as e:
        return jsonify({"error": str(e)})
    else:
        return file


def delete_image(filename: str):
    """Deletes an image."""
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    os.remove(file_path)
    return jsonify({"success": "image deleted"}), 200


def handle_delete_image(filename: str):
    """Deletes the image."""
    try:
        delete = delete_image(filename)
    except (ValueError, TypeError, FileNotFoundError) as e:
        return jsonify({"error": str(e)})
    else:
        return delete


def get_image(filename: str):
    """Load a stored image."""
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    # return file_path
    return send_file(file_path)


def handle_upload_image(file):
    """Handle image upload."""
    try:
        profile_pic = upload_image(file)
    except (ValueError, TypeError) as e:
        raise e
    except Exception as e:
        raise e
    else:
        return profile_pic


def validate_article_data(article_data):
    """Validate article data."""
    if not article_data:
        raise ValueError("The article data must be provided!")
    if not isinstance(article_data, dict):
        raise ValueError("The article data must be a dictionary!")
    valid_keys = [
        "Title",
        "Text",
    ]
    for key in article_data.keys():
        if key not in valid_keys:
            raise ValueError(f"The only valid keys are {valid_keys}")
    if "Title" not in article_data.keys():
        raise ValueError("The Title must be provided")
    if "Text" not in article_data.keys():
        raise ValueError("The Text must be provide!")
