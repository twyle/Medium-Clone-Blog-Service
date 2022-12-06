# -*- coding: utf-8 -*-
"""This module creates the View class and ViewSchema.

1. View class:
    Declares all the functionality used in the creation and manipulation of a
    View.
2. ViewSchema class:
    A meta class that returns the jsonified version of the View class.
"""
from dataclasses import dataclass
from datetime import datetime

from ...extensions import db, ma


@dataclass
class View(db.Model):
    """This model describes an instance of an article being read.

    Attributes
    ---------
    __tablename__: str
        The name of the table represented by this class
    id: int
        The unique identifier for an instance of this class. Primary Key
    author_id:
        The identifier of the creator of this view. Foreign Key
    article_id:
        The identifier of the article that is marked by this view. Foreign Key
    author: The author who created this view.
    article: The article that is marked by this view.
    """

    __tablename__ = "views"
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("Author", backref="views")
    article = db.relationship("Article", backref="views")


class ViewSchema(ma.Schema):
    """Show all the view information."""

    class Meta:
        """The fields to display."""

        fields = (
            "author_id",
            "article_id",
            "date",
        )


view_schema = ViewSchema()
views_schema = ViewSchema(many=True)
