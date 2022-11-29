# -*- coding: utf-8 -*-
import pytest


@pytest.mark.skip(reason="Failing with database not connected!")
def test_health(client):
    """Test the health check route."""
    test_response = client.get("/")
    assert test_response.status_code == 200
