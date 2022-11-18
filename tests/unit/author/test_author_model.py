from api.author.models.author import Author
import pytest
from api import create_app


def test_author_model(author):
    assert author.name == 'Lyle'
    assert author.email_address == 'lyle@gmail.com'
    
 
def test_author_valid_name():
    with create_app().app_context():
        assert Author.validate_name('lyle') is True

   
def test_author_invalid_name():
    with create_app().app_context():
        with pytest.raises(ValueError):
            Author.validate_name('l')
        with pytest.raises(ValueError):
            Author.validate_name(''.join(['a']*30))
        with pytest.raises(ValueError):
            Author.validate_name('')
        with pytest.raises(TypeError):
            Author.validate_name(45)