# -*- coding: utf-8 -*-
# pylint: disable=unexpected-keyword-arg
import os
from typing import Tuple

from flask import jsonify
from sqlalchemy.exc import NoForeignKeysError
from werkzeug.datastructures import FileStorage

from ...author.models.author import Author
from ...extensions import db
from ...helpers.blueprint_helpers import handle_upload_image, validate_article_data
from ...helpers.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from ...tasks import delete_file_s3
from ..models.article import Article, article_schema, articles_schema
from ..models.bookmark import Bookmark, bookmark_schema
from ..models.comment import Comment, comment_schema
from ..models.like import Like, like_schema
from ..models.views import View


def create_article(
    id: str, article_data: dict, article_image: FileStorage
) -> Tuple[str, int]:
    """Create a new article.

    Parameters
    ----------
    id: str
        The authors id
    article_data: dict
        The article details e.g
        {
            'Title': 'Title',
            'Text': 'Text'
        }
    article_image: FileStorage
        The article image

    Raises
    ------
    ValuError:
        When the id is not provided
    TypeError:
        When the id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not id:
        raise ValueError("The id has to be provided.")
    if not isinstance(id, str):
        raise TypeError("The id has to be a string.")
    if not Author.user_with_id_exists(int(id)):
        raise ValueError(f"The author with id {id} does not exist.")
    validate_article_data(article_data)
    Article.validate_title(article_data["Title"])
    Article.validate_text(article_data["Text"])

    article = Article(
        title=article_data["Title"],
        text=article_data["Text"],
        author=Author.get_user(int(id)),
    )

    if article_image:
        if article_image["Image"]:
            profile_pic = handle_upload_image(article_image["Image"])
            article.image = profile_pic

    db.session.add(article)
    db.session.commit()

    return article_schema.dumps(article), HTTP_201_CREATED


def handle_create_article(
    id: str, article_data: dict, pic: FileStorage
) -> Tuple[str, int]:
    """Handle the post request to create a new article.

    Parameters
    ----------
    id: str
        The authors id
    article_data: dict
        The article details e.g
        {
            'Title': 'Title',
            'Text': 'Text'
        }
    pic: FileStorage
        The article image

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        article = create_article(id, article_data, pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    except NoForeignKeysError:
        return jsonify({"error": f"The author with id {id} does not exist."}), 400
    else:
        return article


def get_article(article_id: str, id: str) -> Tuple[str, int]:
    """Get the article with the given id.

    Parameters
    ----------
    article_id: str
        The article id
    id: str
        The author id

    Raises
    ------
    ValuError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not id:
        raise ValueError("The id has to be provided.")
    if not isinstance(id, str):
        raise TypeError("The id has to be a string.")
    if not Author.user_with_id_exists(int(id)):
        raise ValueError(f"The author with id {id} does not exist.")
    if not article_id:
        raise ValueError("The article_id has to be provided.")
    if not isinstance(article_id, str):
        raise TypeError("The article_id has to be a string.")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"The article with id {article_id} does not exist.")
    article = Article.get_article(int(article_id))
    author = Author.get_user(int(id))
    view = View(author=author, article=article)
    db.session.add(view)
    db.session.commit()

    return article_schema.dump(article), HTTP_200_OK


def handle_get_article(article_id: str, author_id: str) -> Tuple[str, int]:
    """Handle GET request to fetch a single article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        author = get_article(article_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return author


def update_article(
    author_id: str, article_id: str, article_data: dict, article_image: FileStorage
) -> Tuple[str, int]:
    """Update a given article.

    Parameters
    ----------
    author_id: str
        The author's id
    article_id: str
        The article id
    article_data: dict
        The article details e.g
        {
            'Title': 'Title',
            'Text': 'Text'
        }
    article_image: FileStorage
        The article image

    Raises
    ------
    ValuError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not author_id:
        raise ValueError("The author_id has to be provided.")
    if not isinstance(author_id, str):
        raise ValueError("The author_id has to be a string.")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"The user with id {author_id} does not exist.")
    if not article_id:
        raise ValueError("The article_id has to be provided.")
    if not isinstance(article_id, str):
        raise TypeError("The article_id has to be a string.")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"The article with id {article_id} does not exist.")
    if (
        not Author.get_user(int(author_id))
        == Article.get_article(int(article_id)).author  # noqa: W503
    ):
        raise ValueError("You can only edit your own articles!")
    if not isinstance(article_data, dict):
        raise TypeError("user_data must be a dict")
    valid_keys = [
        "Title",
        "Text",
    ]
    for key in article_data.keys():
        if key not in valid_keys:
            raise ValueError(f"The only valid keys are {valid_keys}")

    article = Article.get_article(int(article_id))

    if "Title" in article_data.keys():
        Article.validate_title(article_data["Title"])
        article.title = article_data["Title"]
    if "Text" in article_data.keys():
        Article.validate_text(article_data["Text"])

    if article_image:
        if article_image["Image"]:
            if article.image:
                delete_file_s3(os.path.basename(article.image))
            profile_pic = handle_upload_image(article_image["Image"])
            article.image = profile_pic

    db.session.add(article)
    db.session.commit()

    return article_schema.dumps(article), HTTP_200_OK


def delete_article(article_id: str) -> Tuple[str, int]:
    """Delete an article.

    Parameters
    ----------
    article_id: str
        The article id

    Raises
    ------
    ValuError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    return article_schema.dump(Article.delete_article(int(article_id))), HTTP_200_OK


def handle_delete_article(article_id: str) -> Tuple[str, int]:
    """Handle a GET request to delete an article.

    Parameters
    ----------
    article_id: str
        The article id

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        deleted_article = delete_article(article_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)})
    else:
        return deleted_article


def handle_update_article(
    author_id: str, article_id: str, article_data: dict, article_image
) -> Tuple[str, int]:
    """Handle the PUT request to update an article.

    Parameters
    ----------
    author_id: str
        The author's id
    article_id: str
        The article id
    article_data: dict
        The article details e.g
        {
            'Title': 'Title',
            'Text': 'Text'
        }
    article_image: FileStorage
        The article image

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        article = update_article(author_id, article_id, article_data, article_image)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article


def list_articles(author_id: str) -> Tuple[str, int]:
    """List all the articles.

    Parameters
    ----------
    author_id: str, optional
        The author id

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if author_id:
        if not isinstance(author_id, str):
            raise ValueError("The author_id has to be a string.")
        if not Author.user_with_id_exists(int(author_id)):
            raise ValueError(f"The user with id {author_id} does not exist.")
        return articles_schema.dump(Article.all_articles(int(author_id))), HTTP_200_OK
    return articles_schema.dump(Article.all_articles()), HTTP_200_OK


def handle_list_articles(author_id: str) -> Tuple[str, int]:
    """Handle the GET request to list articles.

    Parameters
    ----------
    author_id: str, optional
        The author id

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        articles = list_articles(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return articles


def comments(article_id: str, author_id: str) -> Tuple[str, int]:
    """Coment on an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if author_id:
        if not isinstance(author_id, str):
            raise TypeError("The author id has to be a string")
        if not Author.user_with_id_exists(int(author_id)):
            raise ValueError(f"Their is no author with id {author_id}")
        comments = Article.query.filter_by(id=article_id).first().comments
        art_comments = []
        for comment in comments:
            if comment.author.id == int(author_id):
                art_comments.append(comment)
        return art_comments
    return Article.query.filter_by(id=article_id).first().comments, HTTP_200_OK


def handle_comments(article_id: str, author_id: str) -> Tuple[str, int]:
    """Handle the get request for articles published."""
    try:
        article_comments = comments(article_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return article_comments


def likes(article_id: str) -> Tuple[str, int]:
    """Get all the likes for a given article."""
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    return Article.query.filter_by(id=article_id).first().likes, 200


def handle_likes(article_id: str):
    """Handle the get request for articles published."""
    try:
        article_likes = likes(article_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return article_likes


def bookmarks(article_id: str) -> Tuple[str, int]:
    """Get an article's bookmarks.

    Parameters
    ----------
    article_id: str
        The article's id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    return Article.query.filter_by(id=article_id).first().bookmarks, 200


def handle_bookmarks(article_id: str) -> Tuple[str, int]:
    """Handle the GET request to get an article's bookmarks.

    Parameters
    ----------
    article_id: str
        The article's id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    try:
        article_bookmarks = bookmarks(article_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_bookmarks


def tags(article_id: str) -> Tuple[str, int]:
    """Get the tags for a particular article.

    Parameters
    ----------
    article_id: str
        The article's id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    return (
        jsonify({"Article tags": Article.query.filter_by(id=article_id).first().tags}),
        HTTP_200_OK,
    )


def handle_tags(article_id: str) -> Tuple[str, int]:
    """Handle the GET request to get an article's tags.

    Parameters
    ----------
    article_id: str
        The article's id

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    try:
        article_tags = tags(article_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_tags


def views(article_id: str, author_id: str) -> Tuple[str, int]:
    """Get the data about an article's readership.

    This function lets you know about the authors and
    dates when an article was read.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if author_id:
        if not isinstance(author_id, str):
            raise TypeError("The author id has to be a string")
        if not Author.user_with_id_exists(int(author_id)):
            raise ValueError(f"Their is no author with id {author_id}")
        views = Article.query.filter_by(id=article_id).first().views
        art_views = []
        for view in views:
            if views.author.id == int(author_id):
                art_views.append(view)
        return art_views
    return Article.query.filter_by(id=article_id).first().views, HTTP_200_OK


def handle_views(article_id: str, author_id: str) -> Tuple[str, int]:
    """Handle the GET request to get an articles stats.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    try:
        article_views = views(article_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_views


def article_stats(article_id: str) -> Tuple[str, int]:
    """Get the stats for a given article.

    This includes:
    1. Number of views/reads
    2. Number of likes
    3. Number of comments
    4. The number of bookmarks

    Parameters
    ----------
    article_id: str
        The article's id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    stats = {
        "views": len(Article.query.filter_by(id=article_id).first().views),
        "likes": len(Article.query.filter_by(id=article_id).first().likes),
        "comments": len(Article.query.filter_by(id=article_id).first().comments),
        "bookmarks": len(Article.query.filter_by(id=article_id).first().bookmarks),
    }
    return stats, HTTP_200_OK


def handle_article_stats(article_id: str) -> Tuple[str, int]:
    """Handle the GET request to obtain an article's stats.

    Parameters
    ----------
    article_id: str
        The article's id

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    try:
        stats = article_stats(article_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return stats


def bookmark(article_id: str, author_id: str) -> Tuple[str, int]:
    """Create a bookmark for a given article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if not isinstance(author_id, str):
        raise TypeError("The author id has to be a string")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"Their is no author with id {author_id}")
    if Bookmark.query.filter(
        Bookmark.author_id == int(author_id), Bookmark.article_id == int(article_id)
    ).first():
        raise ValueError("You have already bookmarked this article!")
    author = Author.get_user(int(author_id))
    article = Article.get_article(int(article_id))
    bookmark = Bookmark(article=article, author=author)
    db.session.add(bookmark)
    db.session.commit()
    return bookmark_schema.dump(bookmark), 200


def handle_bookmark(article_id: str, author_id: str) -> Tuple[str, int]:
    """Handle the GET request to bookmark an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    try:
        article_bookmark = bookmark(article_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return article_bookmark


def unbookmark(article_id: str, author_id: str) -> Tuple[str, int]:
    """Delete a bookmark.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if not isinstance(author_id, str):
        raise TypeError("The author id has to be a string")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"Their is no author with id {author_id}")
    if not Bookmark.query.filter(
        Bookmark.author_id == int(author_id), Bookmark.article_id == int(article_id)
    ).first():
        raise ValueError("You have not bookmarked this article!")
    bookmark = Bookmark.query.filter(
        Bookmark.author_id == int(author_id), Bookmark.article_id == int(article_id)
    ).first()
    db.session.delete(bookmark)
    db.session.commit()
    return bookmark_schema.dump(bookmark), 200


def handle_unbookmark(article_id: str, author_id: str) -> Tuple[str, int]:
    """Handle the DELETE request to delete a bookmark.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    try:
        article_bookmark = unbookmark(article_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return article_bookmark


def like(article_id: str, author_id: str) -> Tuple[str, int]:
    """Like an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if not isinstance(author_id, str):
        raise TypeError("The author id has to be a string")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"Their is no author with id {author_id}")
    if Like.query.filter(
        Like.author_id == int(author_id), Like.article_id == int(article_id)
    ).first():
        raise ValueError("You have already liked this article!")
    author = Author.get_user(int(author_id))
    article = Article.get_article(int(article_id))
    like = Like(article=article, author=author)
    db.session.add(like)
    db.session.commit()
    return like_schema.dump(like), HTTP_201_CREATED


def handle_like(article_id: str, author_id: str) -> Tuple[str, int]:
    """Handle the GET request to like an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Returns
    -------
    Tuple[str, int]:
        The json string representing the request
        response as well as the response code.
    """
    try:
        article_like = like(article_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_like


def unlike(article_id: str, author_id: str) -> Tuple[str, int]:
    """Unlike an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if not isinstance(author_id, str):
        raise TypeError("The author id has to be a string")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"Their is no author with id {author_id}")
    if not Like.query.filter(
        Like.author_id == int(author_id), Like.article_id == int(article_id)
    ).first():
        raise ValueError("You have not liked this article!")
    like = Like.query.filter(
        Like.author_id == int(author_id), Like.article_id == int(article_id)
    ).first()
    db.session.delete(like)
    db.session.commit()
    return like_schema.dump(like), HTTP_200_OK


def handle_unlike(article_id: str, author_id: str) -> Tuple[str, int]:
    """Handle DELETE request to delete an article like.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        article_like = unlike(article_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_like


def tag_article(article_id: str, author_id: str, tag: str) -> Tuple[str, int]:
    """Add a tag to an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id
    tag: str
        The tag to remove

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not tag:
        raise ValueError("The tag has to be provided!")
    if not isinstance(tag, str):
        raise TypeError("The tag has to be a string!")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if not isinstance(author_id, str):
        raise TypeError("The author id has to be a string")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"Their is no author with id {author_id}")
    if not Article.get_article(int(article_id)).author_id != int(author_id):
        raise ValueError("You can only tag your articles!")
    if tag in Article.get_article(int(article_id)).tags:
        raise ValueError(f"The article is already tagged as {tag}")
    article = Article.get_article(int(article_id))

    tags = article.tags.copy()
    tags.append(tag)
    article.tags = tags.copy()
    db.session.add(article)
    db.session.commit()
    return (
        jsonify({"article tags": Article.get_article(int(article_id)).tags}),
        HTTP_201_CREATED,
    )


def handle_tag(article_id: str, author_id: str, tag: str) -> Tuple[str, int]:
    """Handle GET request to tag an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id
    tag: str
        The tag to remove

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        article_tag = tag_article(article_id, author_id, tag)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_tag


def untag_article(article_id: str, author_id: str, tag: str) -> Tuple[str, int]:
    """Remove a tag from an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id
    tag: str
        The tag to remove

    Raises
    ------
    ValueError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not tag:
        raise ValueError("The tag has to be provided!")
    if not isinstance(tag, str):
        raise TypeError("The tag has to be a string!")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if not isinstance(author_id, str):
        raise TypeError("The author id has to be a string")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"Their is no author with id {author_id}")
    if not Article.get_article(int(article_id)).author_id != int(author_id):
        raise ValueError("You can only untag your articles!")
    if tag not in Article.get_article(int(article_id)).tags:
        raise ValueError(f"The article is not tagged as {tag}")
    article = Article.get_article(int(article_id))

    tags = article.tags.copy()
    tags.remove(tag)
    article.tags = tags.copy()
    db.session.add(article)
    db.session.commit()
    return (
        jsonify({"article tags": Article.get_article(int(article_id)).tags}),
        HTTP_200_OK,
    )


def handle_untag(article_id: str, author_id: str, tag: str) -> Tuple[str, int]:
    """Handle DELETE request to remove a tag from an artcle.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id
    tag: str
        The tag to remove

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        article_tag = untag_article(article_id, author_id, tag)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_tag


def comment_article(
    article_id: str, author_id: str, comment_data: dict
) -> Tuple[str, int]:
    """Coment on an article.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id
    comment_data: dict
        The dictionary conatining the comment e.g
        {
            'comment': 'Some comment'
        }

    Raises
    ------
    ValuError:
        When the article id is not provided
    TypeError:
        When the article id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not article_id:
        raise ValueError("The article id has to be provided")
    if not isinstance(article_id, str):
        raise TypeError("The article id has to be a string")
    if not Article.article_with_id_exists(int(article_id)):
        raise ValueError(f"Their is no article with id {article_id}")
    if not isinstance(author_id, str):
        raise TypeError("The author id has to be a string")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"Their is no author with id {author_id}")
    if not comment_data:
        raise ValueError("The comment data has to be provided!")
    if not isinstance(comment_data, dict):
        raise TypeError("The comment data has to be a dictionary!")
    if not comment_data["comment"]:
        raise ValueError("The comment data has to be provided!")
    author = Author.get_user(int(author_id))
    article = Article.get_article(int(article_id))
    article_comment = Comment(
        author=author, article=article, comment=comment_data["comment"]
    )
    db.session.add(article_comment)
    db.session.commit()
    return comment_schema.dump(article_comment), HTTP_201_CREATED


def handle_comment(
    article_id: str, author_id: str, comment_data: dict
) -> Tuple[str, int]:
    """Handle POST request to create a comment.

    Parameters
    ----------
    article_id: str
        The article id
    author_id: str
        The author id
    comment_data: dict
        The dictionary conatining the comment e.g
        {
            'comment': 'Some comment'
        }

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        article_comment = comment_article(article_id, author_id, comment_data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_comment


def uncomment_article(comment_id: str, author_id: str) -> Tuple[str, int]:
    """Remove a comment from an article.

    Parameters
    ----------
    comment_id: str
        The comment id
    author_id: str
        The author id

    Raises
    ------
    ValuError:
        When the comment id is not provided.
    TypeError:
        When the comment id is not a string

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    if not comment_id:
        raise ValueError("The comment id has to be provided")
    if not isinstance(comment_id, str):
        raise TypeError("The comment id has to be a string")
    if not Comment.comment_with_id_exists(int(comment_id)):
        raise ValueError(f"Their is no comment with id {comment_id}")
    if not isinstance(author_id, str):
        raise TypeError("The author id has to be a string")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"Their is no author with id {author_id}")
    if not Comment.query.filter_by(author_id=author_id).first().author_id == int(
        author_id
    ):
        raise ValueError("You can only delete your own comments!")
    comment = Comment.query.filter_by(id=comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return comment_schema.dump(comment), HTTP_200_OK


def handle_uncomment(comment_id: str, author_id: str) -> Tuple[str, int]:
    """Handle DELETE request to delete a comment.

    Parameters
    ----------
    comment_id: str
        The comment id
    author_id: str
        The author id

    Returns
    -------
    Tuple[str, int]:
        The jsong string representing the request
        response as well as the response code.
    """
    try:
        article_comment = uncomment_article(comment_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
    else:
        return article_comment
