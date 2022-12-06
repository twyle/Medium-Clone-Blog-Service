# -*- coding: utf-8 -*-
"""This module creates the Bookmark class and BookmarkSchema.

1. Bookmark class:
    Declares all the functionality used in the creation and manipulation of a
    Bookmark.
2. BookmarkSchema class:
    A meta class that returns the jsonified version of the Bookmark class.
"""
from dataclasses import dataclass
from datetime import datetime

from ...extensions import db, ma


@dataclass
class Bookmark(db.Model):
    """The Bookmark Model.

    Attributes
    ---------
    __tablename__: str
        The name of the table represented by this class
    id: int
        The unique identifier for an instance of this class. Primary Key
    author_id:
        The identifier of the creator of this bookmark. Foreign Key
    article_id:
        The identifier of the article that is marked by this bookmark. Foreign Key
    author: The author who created this bookmark
    article: The article that is mrked by this bookmark.
    """

    __tablename__ = "bookmarks"
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("Author", backref="bookmarks")
    article = db.relationship("Article", backref="bookmarks")


class BookmarkSchema(ma.Schema):
    """Show all the bookmark information."""

    class Meta:
        """The fields to display."""

        fields = (
            "author_id",
            "article_id",
            "date",
        )


bookmark_schema = BookmarkSchema()
bookmarks_schema = BookmarkSchema(many=True)
