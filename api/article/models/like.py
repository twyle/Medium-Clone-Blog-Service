from ...extensions import db, ma
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Like(db.Model):
    """The Like Model."""
    __tablename__ = 'likes'
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey('authors.id'))
    article_id: int = db.Column(db.Integer, db.ForeignKey('articles.id'))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    
    author = db.relationship("Author", backref='likes')
    article = db.relationship("Article", backref="likes")