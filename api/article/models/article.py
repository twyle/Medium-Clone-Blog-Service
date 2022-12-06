# -*- coding: utf-8 -*-
"""This module creates the Article class and ArticleSchema.

1. Article class:
    Declares all the functionality used in the creation and manipulation of an
    article.
2. ArticleSchema class:
    A meta class that returns the jsonified version of the Article class.
"""
import os
from dataclasses import dataclass
from datetime import datetime

from flask import current_app
from sqlalchemy.dialects.postgresql import ARRAY

from ...extensions import db, ma
from ...tasks import delete_file_s3


@dataclass
class Article(db.Model):
    """A class used to represent an article.

    Attributes
    ---------
    __tablename__: str
        The name of the table represented by this class
    id: int
        The unique identifier for an instance of this class. Primary Key
    author_id:
        The identifier of the author of this article. Foreign Key
    title: str
        The title of this article
    text: str
        The article contents
    image: str
        The link to the article image
    date_published: datetime
        The date that this article was pblished
    date_edited: datetime
        The last date that this article was edited
    tags: list[str]
        The tags asspciated with this article
    author: Author
        The author of this article
    bookmarks: list[Bookmark]
        A list of all the bookmarks associated with this article.
    comments: list[Comment]
        A list of all the comments associated with this article.
    likes: list[Like]
        A list of all the likes associated with this article.
    views: list[View]
        A list of all the timee this article was read.

    Methods
    -------
    article_with_id_exists(article_id):
        Checks if an article with the given id exists
    validate_title(title):
        Checks if the articlle given is valid.
    validate_text(text):
        Checks if the article contents are valid.
    get_article(article_id: int):
        Fetches a single article.
    all_articles(author_id=None)
        Fetches all the articles.
    delete_article(article_id: int)
        Deletes a single article.
    """

    __tablename__ = "articles"
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    title: str = db.Column(db.String(100), nullable=False)
    text: str = db.Column(db.Text, nullable=False)
    image: str = db.Column(db.String(100), nullable=True)
    date_published: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    date_edited: datetime = db.Column(db.DateTime, nullable=True)
    tags = db.Column(ARRAY(db.String(100)), default=["tech"])

    author = db.relationship("Author", backref="articles_published")

    @staticmethod
    def article_with_id_exists(article_id: int) -> bool:
        """Check if article with given id exists.

        Parameters
        ----------
        article_id: int
            The articles unique identifier.

        Returns
        -------
        bool:
            True if article exists else False
        """
        if Article.query.filter_by(id=article_id).first():
            return True
        return False

    @staticmethod
    def validate_title(title: str) -> bool:
        """Validate the given title.

        Checks if the article is not too short or non-string.

        Parameters
        ----------
        title: str
            The article title to be checked.

        Raises
        ------
        ValueError:
            When the title is not provided
        TypeError:
            When the title is not a string.

        Returns
        -------
        bool:
            True if the title is valid
        """
        if not title:
            raise ValueError("The title has to be provided.")
        if not isinstance(title, str):
            raise TypeError("The title has to be string")
        if len(title) >= current_app.config["TITLE_MAX_LENGTH"]:
            raise ValueError(
                f'The title has to be less than {current_app.config["TITLE_MAX_LENGTH"]}'
            )
        if len(title) <= current_app.config["TITLE_MIN_LENGTH"]:
            raise ValueError(
                f'The title has to be more than {current_app.config["TITLE_MIN_LENGTH"]}'
            )

        return True

    @staticmethod
    def validate_text(text: str) -> bool:
        """Validate the given text.

        Checks if the text is not string.

        Parameters
        ----------
        text: str
            The text to be checked

        Raises
        -----
        ValueError:
            When the text is not provided
        TypeError:
            When the text is not a string.

        Returns
        -------
        bool:
            True if the text is valid
        """
        if not text:
            raise ValueError("The text has to be provided.")
        if not isinstance(text, str):
            raise ValueError("The text has to be string")
        return True

    @staticmethod
    def get_article(article_id: int):
        """Get an article.

        Parameters
        ----------
        article_id: int
            The unique article identifier

        Returns
        -------
        Article:
            The article with the given identifier.
        """
        article = Article.query.filter_by(id=article_id).first()
        return article

    @staticmethod
    def all_articles(author_id=None) -> list:
        """List all articles.

        Parameters
        author_id: int, optional
            The author id whose articles are required.

        Returns
        -------
        list[Articles]:
            All articles or a given author's articles.
        """
        if author_id:
            return Article.query.filter_by(author_id=author_id)
        return Article.query.all()

    @staticmethod
    def delete_article(article_id: int):
        """Delete an article.

        This method also triggers the deletion of the article image from AWS S

        Parameters
        ----------
        article_id: int
            The unique identifier of the article to be deleted.

        Returns
        ------
        Article:
            The article that was deleted.
        """
        article = Article.query.filter_by(id=article_id).first()
        if article.image:
            delete_file_s3(os.path.basename(article.image))
        db.session.delete(article)
        db.session.commit()
        return article


class ArticleSchema(ma.Schema):
    """Show all the article information."""

    class Meta:
        """The fields to display."""

        fields = ("id", "title", "text", "image", "date_published", "tags")


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
