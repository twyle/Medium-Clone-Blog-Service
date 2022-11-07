from ...extensions import db, ma
from datetime import datetime


class Share(db.Model):
    """The Share Model."""
    __tablename__ = 'shares'
    
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey('authors.id'))
    article_id: int = db.Column(db.Integer, db.ForeignKey('articles.id'))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    
    author = db.relationship("Author", backref='shares')
    article = db.relationship("Article", backref="shares")