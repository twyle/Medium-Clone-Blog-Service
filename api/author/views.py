# -*- coding: utf-8 -*-
"""This module contains all the author routes."""
from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from .controller.author import (
    handle_articles_bookmarked,
    handle_articles_commented,
    handle_articles_liked,
    handle_articles_published,
    handle_articles_viewed,
    handle_author_stats,
    handle_create_author,
    handle_delete_author,
    handle_get_author,
    handle_list_authors,
    handle_log_in_author,
    handle_refresh_token,
    handle_update_author,
)

author = Blueprint("author", __name__)


@author.route("/", methods=["POST"])
@swag_from(
    "./docs/register_author.yml", endpoint="author.register_author", methods=["POST"]
)
def register_author():
    """Register an author."""
    return handle_create_author(request.form)


@author.route("/login", methods=["POST"])
@swag_from("./docs/login_user.yml", endpoint="author.login", methods=["POST"])
def login():
    return handle_log_in_author(request.args.get("id"), request.json)


@author.route("/refresh_token", methods=["GET"])
@jwt_required(refresh=True)
@swag_from("./docs/refresh_token.yml", endpoint="author.refresh", methods=["GET"])
def refresh():
    """Generate a refresh token."""
    return handle_refresh_token(get_jwt_identity())


@author.route("/", methods=["GET"])
@jwt_required()
@swag_from("./docs/get_author.yml", endpoint="author.get_author", methods=["GET"])
def get_author():
    """Get a an author by id."""
    return handle_get_author(request.args.get("id"))


@author.route("/", methods=["PUT"])
@jwt_required()
@swag_from("./docs/update_author.yml", endpoint="author.update_author", methods=["PUT"])
def update_author():
    """Update the author with given id."""
    return handle_update_author(request.args.get("id"), request.form)


@author.route("/", methods=["DELETE"])
@jwt_required()
@swag_from(
    "./docs/delete_author.yml", endpoint="author.delete_author", methods=["DELETE"]
)
def delete_author():
    """Delete the author with given id."""
    return handle_delete_author(request.args.get("id"))


@author.route("/authors", methods=["GET"])
@jwt_required()
@swag_from(
    "./docs/get_all_authors.yml", endpoint="author.get_all_authors", methods=["GET"]
)
def get_all_authors():
    """List all authors."""
    return handle_list_authors()


@author.route("/comments", methods=["GET"])
@jwt_required()
@swag_from("./docs/comments.yml", endpoint="author.get_comments", methods=["GET"])
def get_comments():
    """List author comments."""
    return handle_articles_commented(
        request.args.get("id"), request.args.get("article id")
    )


@author.route("/likes", methods=["GET"])
@jwt_required()
@swag_from("./docs/likes.yml", endpoint="author.get_likes", methods=["GET"])
def get_likes():
    """List author likes."""
    return handle_articles_liked(request.args.get("id"))


@author.route("/bookmarks", methods=["GET"])
@jwt_required()
@swag_from("./docs/bookmarks.yml", endpoint="author.get_bookmarks", methods=["GET"])
def get_bookmarks():
    """List author bookmarks."""
    return handle_articles_bookmarked(request.args.get("id"))


@author.route("/articles_published", methods=["GET"])
@jwt_required()
@swag_from(
    "./docs/articles_published.yml",
    endpoint="author.get_articles_published",
    methods=["GET"],
)
def get_articles_published():
    """List author articles published."""
    return handle_articles_published(request.args.get("id"))


@author.route("/articles_read", methods=["GET"])
@jwt_required()
@swag_from(
    "./docs/articles_read.yml", endpoint="author.get_articles_read", methods=["GET"]
)
def get_articles_read():
    """List author articles read."""
    return handle_articles_viewed(request.args.get("id"))


@author.route("/stats", methods=["GET"])
@jwt_required()
@swag_from("./docs/stats.yml", endpoint="author.get_stats", methods=["GET"])
def get_stats():
    """List author articles read."""
    return handle_author_stats(request.args.get("id"))
