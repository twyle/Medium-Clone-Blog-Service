from api.author.controller.author import log_in_author
from api import db
from api import create_app
from api.author.models.author import Author
import pytest

    
def test_login_author():
    author = Author(
        name='Lyle',
        email_address='lyle6@gmail.com'
    )
    with create_app().app_context():
        db.session.add(author)
        db.session.commit()
        
        created_author = Author.query.filter_by(email_address=author.email_address).first()
        
        response = log_in_author(str(created_author.id), author_data={
            'email': 'lyle6@gmail.com'
        })
        
        assert type(response) is tuple
        assert response[1] == 200
        
        logged_in_author = response[0]['author profile']
        assert 'id' in logged_in_author
        assert 'name' in logged_in_author
        assert 'email_address' in logged_in_author
        access_token = response[0]['access token']
        assert type(access_token) is str
        refresh_token = response[0]['refresh token']
        assert type(refresh_token) is str
        
        db.session.delete(created_author)
        db.session.commit()
        
        
def test_login_author_no_id():
    author = Author(
        name='Lyle',
        email_address='lyle7@gmail.com'
    )
    with create_app().app_context():
        db.session.add(author)
        db.session.commit()
        
        created_author = Author.query.filter_by(email_address=author.email_address).first()
        
        with pytest.raises(ValueError):
            response = log_in_author(None, author_data={
                'email': 'lyle7@gmail.com'
            })
        
        db.session.delete(created_author)
        db.session.commit()
        
        
def test_login_author_non_string_id():
    author = Author(
        name='Lyle',
        email_address='lyle8@gmail.com'
    )
    with create_app().app_context():
        db.session.add(author)
        db.session.commit()
        
        created_author = Author.query.filter_by(email_address=author.email_address).first()
        
        with pytest.raises(TypeError):
            response = log_in_author(17, author_data={
                'email': 'lyle5@gmail.com'
            })
        
        db.session.delete(created_author)
        db.session.commit()