from dataclasses import dataclass
from datetime import datetime

from ...extensions import db, ma


@dataclass
class Comment(db.Model):
    """The Comment Model."""

    __tablename__ = "comments"
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    comment: str = db.Column(db.Text, nullable=False)

    author = db.relationship("Author", backref="comments")
    article = db.relationship("Article", backref="comments")

    @staticmethod
    def comment_with_id_exists(comment_id):
        """Check if article with given id exists."""
        if Comment.query.filter_by(id=comment_id).first():
            return True
        return False


class CommentSchema(ma.Schema):
    """Show all the article information."""

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
