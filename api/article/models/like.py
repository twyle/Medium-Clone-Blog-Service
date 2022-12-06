# -*- coding: utf-8 -*-
"""This module creates the Like class and LikeSchema.

1. Like class:
    Declares all the functionality used in the creation and manipulation of a
    Like.
2. LikeSchema class:
    A meta class that returns the jsonified version of the Like class.
"""
from dataclasses import dataclass
from datetime import datetime

from ...extensions import db, ma


@dataclass
class Like(db.Model):
    """The Like Model.

    Attributes
    ---------
    __tablename__: str
        The name of the table represented by this class
    id: int
        The unique identifier for an instance of this class. Primary Key
    author_id:
        The identifier of the creator of this like. Foreign Key
    article_id:
        The identifier of the article that is marked by this like. Foreign Key
    author: The author who created this like
    article: The article that is marked by this like.
    """

    __tablename__ = "likes"
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("Author", backref="likes")
    article = db.relationship("Article", backref="likes")


class LikeSchema(ma.Schema):
    """Show all the like information."""

    class Meta:
        """The fields to display."""

        fields = (
            "author_id",
            "article_id",
            "date",
        )


like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)
