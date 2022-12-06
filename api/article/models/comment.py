# -*- coding: utf-8 -*-
"""This module creates the Comment class and CommentSchema.

1. Comment class:
    Declares all the functionality used in the creation and manipulation of a
    Comment.
2. CommentSchema class:
    A meta class that returns the jsonified version of the Comment class.
"""
from dataclasses import dataclass
from datetime import datetime

from ...extensions import db, ma


@dataclass
class Comment(db.Model):
    """The Comment Model.

    Attributes
    ---------
    __tablename__: str
        The name of the table represented by this class
    id: int
        The unique identifier for an instance of this class. Primary Key
    author_id:
        The identifier of the creator of this comment. Foreign Key
    article_id:
        The identifier of the article to which this comment belongs. Foreign Key
    comment: str
        The comment text.
    author: The author who created this comment
    article: The article to which this comment belongs.

    Methods
    -------
    comment_with_id_exists(comment_id):
        Checks if a comment with the given id exists.
    """

    __tablename__ = "comments"
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    comment: str = db.Column(db.Text, nullable=False)

    author = db.relationship("Author", backref="comments")
    article = db.relationship("Article", backref="comments")

    @staticmethod
    def comment_with_id_exists(comment_id: int) -> bool:
        """Check if article with given id exists.

        Parameters
        ----------
        comment_id: int
            The unique identifier for a given coment

        Returns
        -------
        bool:
            True if comment exists else False
        """
        if Comment.query.filter_by(id=comment_id).first():
            return True
        return False


class CommentSchema(ma.Schema):
    """Show all the comment information."""

    class Meta:
        """The fields to display."""

        fields = (
            "author_id",
            "article_id",
            "comment",
            "date",
        )


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
