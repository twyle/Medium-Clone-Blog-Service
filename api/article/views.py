# -*- coding: utf-8 -*-
"""This module contains all the article routes.

The various functions include:
1. create_article():
    For creating a new article
2. get_article():
    Fetching an article given the id
3. update_article():
    Update an article, given the id
4. delete_article():
    Delete an article, given the id
5. get_all_articles():
    Featch all articles inthe database
6. get_comments():
    Get the comments associated with a given article
7. get_likes():
    Get the likes associated with a given article
8. get_bookmarks():
    Get the bookmarks associated with a given article
9. get_tags():
    Get the tags associated with a given article
10. get_articles_views()
    Get the views for given article
11. get_stats()
    Get the stats for given article
12. bookmark_article()
    Bookmark a given article
13. unbookmark_article()
    Unbookmark a given article
14. handle_like()
    Like a given article
15. handle_unlike()
    Unlike a previously liked article
16. tag_article()
    Add a tag to a given article
17. untag_article()
    Remove a tag from a given article
18. report_article()
    Report an offensive article
19. comment_article()
    Comment on a given article.
20. uncomment_article()
    Delete a comment.
"""
from flasgger import swag_from
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required

from .controller.article import (
    handle_article_stats,
    handle_bookmark,
    handle_bookmarks,
    handle_comment,
    handle_comments,
    handle_create_article,
    handle_delete_article,
    handle_get_article,
    handle_like,
    handle_likes,
    handle_list_articles,
    handle_tag,
    handle_tags,
    handle_unbookmark,
    handle_uncomment,
    handle_unlike,
    handle_untag,
    handle_update_article,
    handle_views,
)

article = Blueprint("article", __name__)


@article.route("/", methods=["POST"])
@jwt_required()
@swag_from(
    "./docs/create_article.yml", endpoint="article.create_article", methods=["POST"]
)
def create_article() -> Response:
    """Create an article."""
    return handle_create_article(request.args.get("id"), request.form, request.files)


@article.route("/", methods=["GET"])
@jwt_required()
@swag_from("./docs/get_article.yml", endpoint="article.get_article", methods=["GET"])
def get_article() -> Response:
    """Get a an article by id."""
    return handle_get_article(request.args.get("id"), request.args.get("author id"))


@article.route("/", methods=["PUT"])
@jwt_required()
@swag_from(
    "./docs/update_article.yml", endpoint="article.update_article", methods=["PUT"]
)
def update_article() -> Response:
    """Update the article with given id."""
    return handle_update_article(
        request.args.get("author id"),
        request.args.get("id"),
        request.form,
        request.files,
    )


@article.route("/", methods=["DELETE"])
@jwt_required()
@swag_from(
    "./docs/delete_article.yml", endpoint="article.delete_article", methods=["DELETE"]
)
def delete_article() -> Response:
    """Delete the article with given id."""
    return handle_delete_article(request.args.get("id"))


@article.route("/articles", methods=["GET"])
@jwt_required()
@swag_from(
    "./docs/get_all_articles.yml", endpoint="article.get_all_articles", methods=["GET"]
)
def get_all_articles() -> Response:
    """List all articles."""
    return handle_list_articles(request.args.get("author id"))


@article.route("/comments", methods=["GET"])
@jwt_required()
@swag_from("./docs/comments.yml", endpoint="article.get_comments", methods=["GET"])
def get_comments() -> Response:
    """List article comments."""
    return handle_comments(request.args.get("id"), request.args.get("author id"))


@article.route("/likes", methods=["GET"])
@jwt_required()
@swag_from("./docs/likes.yml", endpoint="article.get_likes", methods=["GET"])
def get_likes() -> Response:
    """List article likes."""
    return handle_likes(request.args.get("id"))


@article.route("/bookmarks", methods=["GET"])
@jwt_required()
@swag_from("./docs/bookmarks.yml", endpoint="article.get_bookmarks", methods=["GET"])
def get_bookmarks() -> Response:
    """List article bookmarks."""
    return handle_bookmarks(request.args.get("id"))


@article.route("/tags", methods=["GET"])
@jwt_required()
@swag_from("./docs/tags.yml", endpoint="article.get_tags", methods=["GET"])
def get_tags() -> Response:
    """List article tags."""
    return handle_tags(request.args.get("id"))


@article.route("/articles_views", methods=["GET"])
@jwt_required()
@swag_from("./docs/views.yml", endpoint="article.get_articles_views", methods=["GET"])
def get_articles_views() -> Response:
    """List article articles read."""
    return handle_views(request.args.get("id"), request.args.get("author id"))


@article.route("/stats", methods=["GET"])
@jwt_required()
@swag_from("./docs/stats.yml", endpoint="article.get_stats", methods=["GET"])
def get_stats() -> Response:
    """List article articles read."""
    return handle_article_stats(request.args.get("id"))


@article.route("/bookmark", methods=["GET"])
@jwt_required()
@swag_from("./docs/bookmark.yml", endpoint="article.bookmark_article", methods=["GET"])
def bookmark_article() -> Response:
    """Bookmark an article."""
    return handle_bookmark(
        request.args.get("article id"), request.args.get("author id")
    )


@article.route("/unbookmark", methods=["GET"])
@jwt_required()
@swag_from(
    "./docs/unbookmark.yml", endpoint="article.unbookmark_article", methods=["GET"]
)
def unbookmark_article() -> Response:
    """Unbookmark an article."""
    return handle_unbookmark(
        request.args.get("article id"), request.args.get("author id")
    )


@article.route("/like", methods=["GET"])
@jwt_required()
@swag_from("./docs/like.yml", endpoint="article.like_article", methods=["GET"])
def like_article() -> Response:
    """Like an article."""
    return handle_like(request.args.get("article id"), request.args.get("author id"))


@article.route("/unlike", methods=["GET"])
@jwt_required()
@swag_from("./docs/unlike.yml", endpoint="article.unlike_article", methods=["GET"])
def unlike_article() -> Response:
    """Unlike an article."""
    return handle_unlike(request.args.get("article id"), request.args.get("author id"))


@article.route("/tag", methods=["GET"])
@jwt_required()
@swag_from("./docs/tag.yml", endpoint="article.tag_article", methods=["GET"])
def tag_article() -> Response:
    """Tag an article."""
    return handle_tag(
        request.args.get("article id"),
        request.args.get("author id"),
        request.args.get("tag"),
    )


@article.route("/untag", methods=["GET"])
@jwt_required()
@swag_from("./docs/untag.yml", endpoint="article.untag_article", methods=["GET"])
def untag_article() -> Response:
    """Untag an article."""
    return handle_untag(
        request.args.get("article id"),
        request.args.get("author id"),
        request.args.get("tag"),
    )


@article.route("/report", methods=["POST"])
@jwt_required()
@swag_from("./docs/report.yml", endpoint="article.report_article", methods=["POST"])
def report_article() -> Response:
    """Report an article."""
    # return handle_create_article(request.form, request.files)
    return jsonify({"success": "report article"})


@article.route("/comment", methods=["POST"])
@jwt_required()
@swag_from("./docs/comment.yml", endpoint="article.comment_article", methods=["POST"])
def comment_article() -> Response:
    """Comment an article."""
    return handle_comment(
        request.args.get("article id"), request.args.get("author id"), request.json
    )


@article.route("/uncomment", methods=["GET"])
@jwt_required()
@swag_from(
    "./docs/uncomment.yml", endpoint="article.uncomment_article", methods=["GET"]
)
def uncomment_article() -> Response:
    """Comment an article."""
    return handle_uncomment(
        request.args.get("comment id"), request.args.get("author id")
    )
