# -*- coding: utf-8 -*-
import json

import pytest

from api import create_app
from api.author.controller.author import create_author
from api.author.controller.helper import validate_author_data
from api.helpers.exceptions import AuthorExists


def test_validate_author_data_valid():
    author_data = {"Name": "Lyle", "Email Address": "lyle@gmail.com"}
    assert validate_author_data(author_data) is True


def test_validate_author_data_empty_data():
    with pytest.raises(ValueError):
        validate_author_data({})


def test_validate_author_data_non_dictionary_data():
    with pytest.raises(ValueError):
        validate_author_data("")


def test_validate_author_data_non_valid_keys():
    with pytest.raises(ValueError):
        validate_author_data({"a": "b"})


def test_validate_author_data_missing_name():
    with pytest.raises(ValueError):
        validate_author_data({"Email Address": "lyle@gmail.com"})


def test_validate_author_data_missing_email():
    # Misiing email
    with pytest.raises(ValueError):
        validate_author_data({"Name": "Lyle"})


def test_validate_author_data_empty_name():
    with pytest.raises(ValueError):
        validate_author_data({"Name": "", "Email Address": "lyle@gmail.com"})


def test_validate_author_data_empty_email():
    with pytest.raises(ValueError):
        validate_author_data({"Name": "Lyle", "Email Address": ""})


def test_create_author():
    with create_app().app_context():
        author_data = {"Name": "Lyle", "Email Address": "lyle@gmail.com"}
        response = create_author(author_data)
        assert type(response) is tuple
        assert response[1] == 201
        created_author = json.loads(response[0])
        assert created_author["name"] == "Lyle"
        assert created_author["email_address"] == "lyle@gmail.com"


def test_create_author_existing_author():
    with create_app().app_context():
        author_data = {"Name": "Lyle1", "Email Address": "lyle1@gmail.com"}
        create_author(author_data)
        with pytest.raises(AuthorExists):
            create_author(author_data)


def test_create_author_route(client):
    author_data = {"Name": "Lyle", "Email Address": "lyle2@gmail.com"}
    with create_app().app_context():
        response = client.post("/author/", data=author_data)
        assert response.status_code == 201
        created_author = json.loads(response.text)
        assert "id" in created_author
        assert "name" in created_author
        assert "email_address" in created_author
        assert created_author["name"] == "Lyle"
        assert created_author["email_address"] == "lyle2@gmail.com"


def test_create_author_route_existing_author(client):
    author_data = {"Name": "Lyle", "Email Address": "lyle3@gmail.com"}
    with create_app().app_context():
        response = client.post("/author/", data=author_data)
        assert response.status_code == 201
        response = client.post("/author/", data=author_data)
        assert response.status_code == 409
