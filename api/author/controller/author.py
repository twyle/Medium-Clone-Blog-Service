from .helper import validate_author_data
from ..models.author import Author, author_schema, authors_schema
from ...extensions import db
from flask import jsonify, current_app
from ...article.models.article import Article
import json
from flask_jwt_extended import create_access_token, create_refresh_token
from ...helpers.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_409_CONFLICT
)
from ...helpers.exceptions import (
    AuthorExists,
    AuthorDoesNotExist
)


def create_author(author_data: dict):
    """Handle the post request to create a new author."""
    
    validate_author_data(author_data)
    
    Author.validate_name(author_data['Name'])
    Author.validate_email(author_data['Email Address'])
        
    if Author.user_with_email_exists(author_data["Email Address"]):
        raise AuthorExists(f'The author with email address {author_data["Email Address"]} exists')
    
    author = Author(
        name=author_data["Name"],
        email_address=author_data["Email Address"],
    )
        
    db.session.add(author)
    db.session.commit()

    return author_schema.dumps(author), HTTP_201_CREATED


def handle_create_author(author_data: dict):
    """Handle the post request to create a new author."""
    try:
        author = create_author(author_data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except AuthorExists as e:
        return jsonify({"error": str(e)}), HTTP_409_CONFLICT
    else:
        return author
    

def log_in_author(author_id: str, author_data: dict):
    """Log in a registered user."""
    if not author_id:
        raise ValueError(f"The authorid has to be provided!")
    if not isinstance(author_id, str):
        raise TypeError(f"The authorid has to be a string")
    if not author_data:
        raise ValueError(f"The author data cannot be empty.")
    if not isinstance(author_data, dict):
        raise TypeError("author_data must be a dict")
    if "email" not in author_data.keys():
        raise ValueError(f"The email is missing from the authordata")
    if not author_data["email"]:
        raise ValueError(f"The email data for authoris missing")
    if not Author.user_with_email_exists(author_data["email"]):
        raise AuthorDoesNotExist(
            f'The author with email {author_data["email"]} does not exist!'
        )
    if not Author.validate_user(int(author_id), author_data["email"]):
        raise AuthorDoesNotExist(
            f'The authorwith email {author_data["email"]} and id {author_id} does not exist!'
        )

    author = Author.query.filter_by(email_address=author_data["email"]).first()
    if author:
        access_token = create_access_token(identity=author.id)
        refresh_token = create_refresh_token(identity=author.id)
        author_data = {
            'author profile': json.loads(author_schema.dumps(author)),
            'access token': access_token,
            'refresh token': refresh_token
        }

        return author_data, HTTP_200_OK


def handle_log_in_author(author_id: str, author_data: dict) -> dict:
    """Handle a POST request to log in an admin."""
    try:
        data = log_in_author(author_id, author_data)
    except (
        ValueError,
        TypeError
    ) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return data

    
def get_author(author_id: str) -> dict:
    """Get the user with the given id."""
    if not author_id:
        raise ValueError("The author_id has to be provided.")
    if not isinstance(author_id, str):
        raise TypeError("The author_id has to be a string.")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"The user with id {author_id} does not exist.")

    return author_schema.dump(Author.get_user(int(author_id))), 200   

    
def handle_get_author(author_id: str):
    """Get a single author."""
    try:
        author = get_author(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return author


def delete_author(author_id: str):
    """Delete an author."""
    if not author_id:
        raise ValueError('The author id has to be provided')
    if not isinstance(author_id, str):
        raise TypeError('The author id has to be a string')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'Their is no author with id {author_id}')
    return author_schema.dump(Author.delete_user(int(author_id))), 200


def handle_delete_author(author_id: str):
    """List all authors."""
    try:
        deleted_author = delete_author(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)})
    else:
        return deleted_author


def update_author(author_id: str, author_data: dict):
    """Handle the post request to create a new author."""
    if not author_id:
        raise ValueError("The author_id has to be provided.")
    if not isinstance(author_id, str):
        raise ValueError("The author_id has to be a string.")
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f"The user with id {author_id} does not exist.")
    if not isinstance(author_data, dict):
        raise TypeError("author_data must be a dict")
    valid_keys = [
        "Name",
        "Email Address",
    ]
    for key in author_data.keys():
        if key not in valid_keys:
            raise ValueError(f"The only valid keys are {valid_keys}")
    
    author = Author.get_user(int(author_id))
    
    if "Name" in author_data.keys():
        Author.validate_name(author_data['Name'])
        author.name = author_data['Name']
    if "Email Address" in author_data.keys():
        Author.validate_email(author_data['Email Address'])
        if Author.user_with_email_exists(author_data["Email Address"]):
            raise ValueError(f'The user with email address {author_data["Email Address"]} exists')
        author.email_address = author_data['Email Address']
        
    db.session.add(author)
    db.session.commit()

    return author_schema.dumps(author), 201


def handle_update_author(author_id: str, author_data: dict):
    """Handle the post request to create a new author."""
    try:
        author = update_author(author_id, author_data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return author
    

def handle_list_authors():
    """List all authors."""
    return authors_schema.dump(Author.query.all()), HTTP_200_OK


def articles_published(author_id: str):
    """Delete an author."""
    if not author_id:
        raise ValueError('The author id has to be provided')
    if not isinstance(author_id, str):
        raise TypeError('The author id has to be a string')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'Their is no author with id {author_id}')
    return Author.query.filter_by(id=author_id).first().articles_published, 200


def handle_articles_published(author_id: str):
    """Handle the get request for articles published."""
    try:
        articles = articles_published(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return articles
    

def articles_bookmarked(author_id: str):
    """Delete an author."""
    if not author_id:
        raise ValueError('The author id has to be provided')
    if not isinstance(author_id, str):
        raise TypeError('The author id has to be a string')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'Their is no author with id {author_id}')
    return Author.query.filter_by(id=author_id).first().bookmarks, 200


def handle_articles_bookmarked(author_id: str):
    """Handle the get request for articles published."""
    try:
        bookmarks = articles_bookmarked(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return bookmarks
    
def articles_commented(author_id: str, article_id: str):
    """Delete an author."""
    if not author_id:
        raise ValueError('The author id has to be provided')
    if not isinstance(author_id, str):
        raise TypeError('The author id has to be a string')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'Their is no author with id {author_id}')
    if article_id:
        if not isinstance(article_id, str):
            raise TypeError('The article id has to be a string')
        if not Article.article_with_id_exists(int(article_id)):
            raise ValueError(f'Their is no article with id {article_id}')
        comments = Author.query.filter_by(id=author_id).first().comments
        art_comments = []
        for comment in comments:
            if comment.article.id == int(article_id):
                art_comments.append(comment)
        return art_comments
    return Author.query.filter_by(id=author_id).first().comments, 200


def handle_articles_commented(author_id: str, article_id: str):
    """Handle the get request for articles published."""
    try:
        comments = articles_commented(author_id, article_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return comments


def articles_liked(author_id: str):
    """Delete an author."""
    if not author_id:
        raise ValueError('The author id has to be provided')
    if not isinstance(author_id, str):
        raise TypeError('The author id has to be a string')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'Their is no author with id {author_id}')
    return Author.query.filter_by(id=author_id).first().likes, 200


def handle_articles_liked(author_id: str):
    """Handle the get request for articles published."""
    try:
        likes = articles_liked(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return likes
    
def articles_viewed(author_id: str):
    """Delete an author."""
    if not author_id:
        raise ValueError('The author id has to be provided')
    if not isinstance(author_id, str):
        raise TypeError('The author id has to be a string')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'Their is no author with id {author_id}')
    return Author.query.filter_by(id=author_id).first().views, 200


def handle_articles_viewed(author_id: str):
    """Handle the get request for articles published."""
    try:
        views = articles_viewed(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return views


def author_stats(author_id: str):
    """Delete an author."""
    if not author_id:
        raise ValueError('The author id has to be provided')
    if not isinstance(author_id, str):
        raise TypeError('The author id has to be a string')
    if not Author.user_with_id_exists(int(author_id)):
        raise ValueError(f'Their is no author with id {author_id}')
    stats = {
        'views': len(Author.query.filter_by(id=author_id).first().views),
        'likes': len(Author.query.filter_by(id=author_id).first().likes),
        'comments': len(Author.query.filter_by(id=author_id).first().comments),
        'articles published': len(Author.query.filter_by(id=author_id).first().articles_published), 
        'bookmarks': len(Author.query.filter_by(id=author_id).first().bookmarks)
    }
    return stats, 200


def handle_author_stats(author_id: str):
    """Handle the get request for articles published."""
    try:
        stats = author_stats(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return stats


def handle_refresh_token(identity) -> dict:
    """Generate a new access token."""
    return jsonify(access_token=create_access_token(identity=identity)), 200