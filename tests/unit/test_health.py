# -*- coding: utf-8 -*-
def test_health(client):
    """Test the health check route."""
    test_response = client.get("/")
    assert test_response.status_code == 200
