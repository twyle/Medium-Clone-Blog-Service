# -*- coding: utf-8 -*-
"""Declare the celery tasks."""
from ..extensions import s3
from flask import current_app
import os
from botocore.exceptions import ClientError

# @celery.task(name="delete_image")
def delete_file_s3(filename):
    """Delete profile pic."""
    s3.delete_object(
        Bucket=current_app.config["S3_BUCKET"], Key=filename
    )


# @celery.task(name="upload_image")
def upload_file_to_s3(filename):
    """Upload a file to S3."""

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'rb') as profilepic:
        try:
            s3.upload_fileobj(profilepic, current_app.config['S3_BUCKET'], filename, ExtraArgs={'ACL': 'public-read'})
            # s3.upload_fileobj(profilepic, current_app.config['S3_BUCKET'], filename)
            os.remove(filepath)
        except ClientError as e: 
            print(str(e))

    data = f"{current_app.config['S3_LOCATION']}{filename}"
    return {"image": data}
