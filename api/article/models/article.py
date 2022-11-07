from ...extensions import db, ma
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from dataclasses import dataclass


@dataclass
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
    
    @staticmethod
    def article_with_id_exists(article_id):
        """Check if article with given id exists."""
        if Article.query.filter_by(id=article_id).first():
            return True
        return False
    

class ArticleSchema(ma.Schema):
    """Show all the article information."""

    class Meta:
        """The fields to display."""

        fields = (
            "id",
            "title",
            "text",
            "image",
            "date_published",
            "tags"
        )

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
    
    