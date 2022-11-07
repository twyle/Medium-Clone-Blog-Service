from ...extensions import db, ma
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY


class Article(db.Model):
    """The article class"""
    
    __tablename__ = 'articles'
    
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey('authors.id'))
    title: str = db.Column(db.String(100), nullable=False)
    text: str = db.Column(db.Text, nullable=False)
    image: str = db.Column(db.String(100), nullable=True)
    date_published: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    date_edited: datetime = db.Column(db.DateTime, nullable=True)
    tags = db.Column(ARRAY(db.String(100)), default=['tech'])
    
    author = db.relationship("Author", backref='articles_published')
    
    