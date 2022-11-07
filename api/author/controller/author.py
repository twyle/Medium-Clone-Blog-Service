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
        raise TypeError("user_data must be a dict")
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
    return authors_schema.dump(Author.all_users()), 200