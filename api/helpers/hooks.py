from flask import request
from ..config import app_logger
from flask import request
import json


def log_post_request():
    request_data = {
        'method': request.method,
        'url root': request.url_root,
        'user agent': request.user_agent,
        'scheme': request.scheme,
        'remote address': request.remote_addr,
        'headers': request.headers,
    }
    if request.args:
        request_data['args'] = request.args
    if request.form:
        request_data['data'] = request.form
    else:
        request_data['data'] = request.json
    if request.cookies:
        request_data['cookies'] = request.cookies
    if request.files:
        request_data['image'] = {
            'filename': request.files['Image'].filename,
            'content type': request.files['Image'].content_type,
            'size': len(request.files['Image'].read())//1000,
        }
    app_logger.info(str(request_data))



def log_get_request():
    request_data = {
        'method': request.method,
        'url root': request.url_root,
        'user agent': request.user_agent,
        'scheme': request.scheme,
        'remote address': request.remote_addr,
        'headers': request.headers,
        'route': request.endpoint,
        'base url': request.base_url,
        'url': request.url
    }
    if request.args:
        request_data['args'] = request.args
    if request.cookies:
        request_data['cookies'] = request.cookies
    app_logger.info(str(request_data))
    
    
def get_response(response):
    response_data = {
        'status': response.status,
        'status code': response.status_code,
        'response': json.loads(response.data)
    }
    app_logger.info(str(response_data))
    
    
def get_exception(exc):
    """Log exceptions"""
    if exc:
        app_logger.warning(f'{exc.__class__.__name__ }: {str(exc)}')