from dataclasses import dataclass
from datetime import datetime

from ...extensions import db, ma


@dataclass
class Bookmark(db.Model):
    """The Bookmark Model."""

    __tablename__ = "bookmarks"

    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("Author", backref="bookmarks")
    article = db.relationship("Article", backref="bookmarks")


class BookmarkSchema(ma.Schema):
    """Show all the article information."""

    class Meta:
        """The fields to display."""

        fields = (
            "author_id",
            "author_id",
            "date",
        )


bookmark_schema = BookmarkSchema()
bookmarks_schema = BookmarkSchema(many=True)
