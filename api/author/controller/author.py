from .helper import validate_user_data
from ..models.author import Author, author_schema, authors_schema
from ...extensions import db
from flask import jsonify


def create_author(author_data: dict):
    """Handle the post request to create a new author."""
    
    validate_user_data(author_data)
    
    Author.validate_name(author_data['Name'])
    Author.validate_email(author_data['Email Address'])
        
    if Author.user_with_email_exists(author_data["Email Address"]):
        raise ValueError(f'The user with email address {author_data["Email Address"]} exists')
    
    author = Author(
        name=author_data["Name"],
        email_address=author_data["Email Address"],
    )
        
    db.session.add(author)
    db.session.commit()

    return author_schema.dumps(author), 201


def handle_create_author(author_data: dict):
    """Handle the post request to create a new author."""
    try:
        author = create_author(author_data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return author