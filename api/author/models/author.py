from ...extensions import db, ma
from dataclasses import dataclass
from flask import current_app
from ..controller.helper import is_email_address_format_valid

@dataclass
class Author(db.Model):
    """The author class"""
    
    __tablename__ = 'authors'
    
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    email_address: str = db.Column(db.Text, nullable=False, unique=True)
    
    @staticmethod
    def user_with_id_exists(user_id):
        """Check if user with given id exists."""
        if Author.query.filter_by(id=user_id).first():
            return True
        return False
    
    @staticmethod
    def user_with_email_exists(user_email):
        """Check if user with given email exists."""
        if Author.query.filter_by(email_address=user_email).first():
            return True
        return False
    
    @staticmethod
    def validate_name(user_name):
        """Validate the given name."""
        if not user_name:
            raise ValueError("The user_name has to be provided.")

        if not isinstance(user_name, str):
            raise TypeError("The user_name has to be string")

        if len(user_name) >= current_app.config["NAME_MAX_LENGTH"]:
            raise ValueError(
                f'The user_name has to be less than {current_app.config["NAME_MAX_LENGTH"]}'
            )

        if len(user_name) <= current_app.config["NAME_MIN_LENGTH"]:
            raise ValueError(
                f'The user_name has to be more than {current_app.config["NAME_MIN_LENGTH"]}'
            )

        return True
        
    
    @staticmethod
    def validate_email(email):
        """Validate the given name."""
        return is_email_address_format_valid(email)
    
    
    @staticmethod   
    def validate_user(id, email):
        """Check if user id and email belong to the same person."""
        if not id:
            raise ValueError("The user id has to be provided!")

        if not isinstance(id, int):
            raise ValueError("The id has to be an int")

        if not email:
            raise ValueError("The email has to be provided.")

        if not isinstance(email, str):
            raise ValueError("The user_email has to be an string")

        user = Author.query.filter_by(id=id).first()

        if user.email_address == email:
            return True


    
    @staticmethod   
    def all_users():
        """List all users."""
        return Author.query.all()
    
    @staticmethod    
    def delete_user(user_id: int):
        """Delete a user."""
        user = Author.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return user
    
    @staticmethod   
    def get_user(user_id: int):
        """Get a user."""
        user = Author.query.filter_by(id=user_id).first()
        return user 

    
class AuthorSchema(ma.Schema):
    """Show all the user information."""

    class Meta:
        """The fields to display."""

        fields = (
            "id",
            "name",
            "email_address",
        )

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
    
    