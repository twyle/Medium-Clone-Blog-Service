# -*- coding: utf-8 -*-
"""This module contains all the author routes."""
from flasgger import swag_from
from flask import Blueprint, request, jsonify
# from .controller import (
#     handle_list_authors,
#     handle_delete_author,
#     handle_get_author,
#     handle_update_author
# )

author = Blueprint("author", __name__)


@swag_from(
    "./docs/register_author.yml", endpoint="author.register_author", methods=["POST"]
)
@author.route("/", methods=["POST"])
def register_author():
    """Register an author."""
    # return handle_create_author(request.form, request.files)
    return jsonify({'success': 'register author'})


@swag_from("./docs/get_author.yml", endpoint="author.get_author", methods=["GET"])
@author.route("/", methods=["GET"])
def get_author():
    """Get a an author by id."""
    # return handle_get_author(request.args.get('id'))
    return jsonify({'success': 'get author'})


@swag_from("./docs/update_author.yml", endpoint="author.update_author", methods=["PUT"])
@author.route("/", methods=["PUT"])
def update_author():
    """Update the author with given id."""
    # return handle_update_author(request.args.get("id"), request.form)
    return jsonify({'success': 'update author'})


@swag_from(
    "./docs/delete_author.yml", endpoint="author.delete_author", methods=["DELETE"]
)
@author.route("/", methods=["DELETE"])
def delete_author():
    """Delete the author with given id."""
    # return handle_delete_author(request.args.get('id'))
    return jsonify({'success': 'delete author'})



@swag_from(
    "./docs/get_all_authors.yml", endpoint="author.get_all_authors", methods=["GET"]
)
@author.route("/authors", methods=["GET"])
def get_all_authors():
    """List all authors."""
    # return handle_list_authors()
    return jsonify({'success': 'list authors'})
