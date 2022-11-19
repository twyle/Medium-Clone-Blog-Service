import pytest

from api.author.models.author import Author


@pytest.fixture()
def author():
    """Create an author."""
    author = Author(name="Lyle", email_address="lyle@gmail.com")
    return author
