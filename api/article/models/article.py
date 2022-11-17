from ...extensions import db, ma
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from dataclasses import dataclass
from flask import current_app
import os
from ...tasks import delete_file_s3


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
    
    @staticmethod
    def validate_title(title):
        """Validate the given title."""
        if not title:
            raise ValueError("The title has to be provided.")
        if not isinstance(title, str):
            raise ValueError("The title has to be string")
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
    def validate_text(text):
        """Validate the given text."""
        if not text:
            raise ValueError("The text has to be provided.")
        if not isinstance(text, str):
            raise ValueError("The text has to be string")
        return True
    
    @staticmethod   
    def get_article(article_id: int):
        """Get an article."""
        article = Article.query.filter_by(id=article_id).first()
        return article
    
    
    @staticmethod   
    def all_articles(author_id=None):
        """List all users."""
        if author_id:
            return Article.query.filter_by(author_id=author_id)
        return Article.query.all()
    
    
    @staticmethod  
    def delete_article(article_id: int):
        """Delete an article."""
        article = Article.query.filter_by(id=article_id).first()
        if article.image:
            # delete_file_s3.delay(os.path.basename(author.profile_picture))
            delete_file_s3(os.path.basename(article.image))
        db.session.delete(article)
        db.session.commit()
        return article
    

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
    
    