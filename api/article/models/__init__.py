# -*- coding: utf-8 -*-
"""Declares all the models used by the article blueprint.

The models include:
1. Article:
    Describes an article including it's author, title, text
    image and publication date.
2. Bookmark:
    Describes an article bookmark, including the article,
    the author and the date bookmarked.
3. Comment:
    Describes a comment on an article, including the author,
    the article and the date of the comment as well as the
    comment text.
4. Like:
    Describes a like, including the author, article and the
    date.
5. Share: TODO
6. View:
    Describes a instance when an article is read and consists
    of an author, article and the date.
"""
from .article import Article
from .bookmark import Bookmark
from .comment import Comment
from .like import Like
from .share import Share
from .views import View

__all__ = ["Article", "Bookmark", "Comment", "Like", "Share", "View"]
