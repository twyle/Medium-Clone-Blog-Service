from dataclasses import dataclass
from datetime import datetime

from ...extensions import db, ma


@dataclass
class Like(db.Model):
    """The Like Model."""

    __tablename__ = "likes"
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("Author", backref="likes")
    article = db.relationship("Article", backref="likes")


class LikeSchema(ma.Schema):
    """Show all the article information."""

    class Meta:
        """The fields to display."""

        fields = (
            "author_id",
            "author_id",
            "date",
        )


like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)
