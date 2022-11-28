# -*- coding: utf-8 -*-
import json

import pytest

from api import create_app


@pytest.fixture()
def create_author(client):
    created_author = None
    author_data = {"Name": "Lyle", "Email Address": "lyle8@gmail.com"}
    with create_app().app_context():
        response = client.post("/author/", data=author_data)
        assert response.status_code == 201
        created_author = json.loads(response.text)
    return created_author


def login(author, client):
    with create_app().app_context():
        response = client.post(
            "/author/login",
            query_string={"id": str(author["id"])},
            json={"email": author["email_address"]},
        )
        assert response.status_code == 200
        response_data = json.loads(response.text)
        assert "access token" in response_data
        assert "refresh token" in response_data
        assert "author profile" in response_data


def test_signup_login(create_author, client):
    login(create_author, client)
