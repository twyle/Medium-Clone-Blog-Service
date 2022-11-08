from .helpers import validate_article_data
from ..models.article import (
    Article, article_schema, articles_schema
)
from flask import jsonify
from ...author.models.author import Author
from ...extensions import db
from sqlalchemy.exc import NoForeignKeysError
from ..models.views import View


def create_article(id: str, article_data: dict, pic):
    """Handle the post request to create a new article."""
    if not id:
        raise ValueError("The id has to be provided.")
    if not isinstance(id, str):
        raise TypeError("The id has to be a string.")
    if not Author.user_with_id_exists(int(id)):
        raise ValueError(f"The author with id {id} does not exist.")
    validate_article_data(article_data)
    Article.validate_title(article_data['Title'])
    Article.validate_text(article_data['Text'])
    
    article = Article(
        title=article_data["Title"],
        text=article_data["Text"],
        author=Author.get_user(int(id))
    )
        
    db.session.add(article)
    db.session.commit()

    return article_schema.dumps(article), 201


def handle_create_article(id: str, article_data: dict, pic):
    """Handle the post request to create a new article."""
    try:
        article = create_article(id, article_data, pic)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except NoForeignKeysError:
        return jsonify({"error": f"The author with id {id} does not exist."}), 400
    else:
        return article
    
def get_article(article_id: str, id: str) -> dict:
    """Get the user with the given id."""
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
    author=Author.get_user(int(id))
    view = View(author=author, article=article)
    db.session.add(view)
    db.session.commit()

    return article_schema.dump(article), 200   

    
def handle_get_article(article_id: str, author_id: str):
    """Get a single author."""
    try:
        author = get_article(article_id, author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return author
    

def update_article(author_id: str, article_id: str, article_data: dict):
    """Handle the post request to create a new author."""
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
    if not Author.get_user(int(author_id)) == Article.get_article(int(article_id)).author:
        raise ValueError('You can only edit your own articles!')
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
        Article.validate_title(article_data['Title'])
        article.title = article_data['Title']
    if "Text" in article_data.keys():
        Article.validate_text(article_data['Text'])
        
    db.session.add(article)
    db.session.commit()

    return article_schema.dumps(article), 201


def handle_update_article(author_id: str, article_id: str, article_data: dict):
    """Handle the post request to create a new author."""
    try:
        article = update_article(author_id, article_id, article_data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return article
    
    
def list_articles(author_id: str):
    if author_id:
        if not isinstance(author_id, str):
            raise ValueError("The author_id has to be a string.")
        if not Author.user_with_id_exists(int(author_id)):
            raise ValueError(f"The user with id {author_id} does not exist.") 
        return articles_schema.dump(Article.all_articles(int(author_id))), 200 
    return articles_schema.dump(Article.all_articles()), 200  
    

def handle_list_articles(author_id: str):
    """List all authors."""
    try:
        articles = list_articles(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return articles