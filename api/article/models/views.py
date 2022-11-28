# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime

from ...extensions import db


@dataclass
class View(db.Model):
    """This model describes an instance of an article being read."""

    __tablename__ = "views"
    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"))
    article_id: int = db.Column(db.Integer, db.ForeignKey("articles.id"))
    date: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("Author", backref="views")
    article = db.relationship("Article", backref="views")
