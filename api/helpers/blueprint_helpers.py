# -*- coding: utf-8 -*-
"""This module declares methods used by the blueprints.

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
4. save_image():
    Saves an image locally.
5. handle_upload_image():
    Handles the GET request to fetch an image stored locally.
6. validate_article_data():
    Checks the article data to ensure that all the required
    fields are present.
7. delete_image():
    Deletes an image stored locally.
8. handle_delete_image()
    Handles the DELETE request to delete an image stored
    locally.
"""
import os

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ..tasks import upload_file_to_s3


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


def upload_image(file: FileStorage) -> str:
    """Trigger the upload of image to s3.

    Parameters
    ----------
    file: FileStorage
        The file to be uploaded to s3

    Raises
    ------
        Valuerror:
            Whenimage is not provided
        TypeError:
            When ht filename is missing

    Returns
    -------
    str:
        The link to the uploaded image
    """
    if not file:
        raise ValueError("The file has to be provided!")
    if file.filename == "":
        raise ValueError("The file has to be provided!")
    if not allowed_file(file.filename):
        raise TypeError("That file type is not allowed!")
    try:
        save_image(file)
    except (ValueError, TypeError) as e:
        raise e
    upload_file_to_s3(file.filename)
    profile_pic = f"{current_app.config['S3_LOCATION']}{file.filename}"
    return profile_pic


def handle_upload_image(file: FileStorage) -> str:
    """Handle image upload.

    Handles the request to upload the image.

    file: FileStorage
        The file to be uploaded to s3

    Returns
    -------
    profile_pic: str
        The link to the profile image.
    """
    try:
        profile_pic = upload_image(file)
    except (ValueError, TypeError) as e:
        raise e
    except Exception as e:
        raise e
    else:
        return profile_pic


def validate_article_data(article_data: dict) -> None:
    """Validate article data.

    Ensure that the data provided by the user contains
    all the fields needed to create a new article.

    Parameters
    ----------
    article_data: dict
        A dictionary containing the fields used to create
        a new article. e.g
        {
            'Title': 'Some Title',
            'Text': 'Some text'
        }

    Raises
    ------
    ValuError:
    TypeError:

    Return
    ------
    bool:
        True if the article data is good else False
    """
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
