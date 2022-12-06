# -*- coding: utf-8 -*-
"""This module creates the Share class and ShareSchema.

1. Share class:
    Declares all the functionality used in the creation and manipulation of a
    Share.
2. ShareSchema class:
    A meta class that returns the jsonified version of the Share class.
"""
from datetime import datetime

from ...extensions import db


class Share(db.Model):
    """The Share Model.

    This class models the act of sharing an article e.g to twitter.

    Attributes
    ---------
    __tablename__: str
        The name of the table represented by this class
    id: int
        The unique identifier for an instance of this class. Primary Key
    author_id:
        The identifier of the creator of this share. Foreign Key
    article_id:
        The identifier of the article that is shared. Foreign Key
    author: The author who created this share.
    article: The article that is shared.
    """

    __tablename__ = "shares"

    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("Author", backref="shares")
    article = db.relationship("Article", backref="shares")
