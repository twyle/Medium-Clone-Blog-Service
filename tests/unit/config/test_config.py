# -*- coding: utf-8 -*-
def test_testing_config(app):
    """Test the test configuration."""
    assert app.config["TESTING"] is True


def test_development_config(dev_app):
    """Test the development configuration."""
    assert dev_app.config["TESTING"] is False
