# -*- coding: utf-8 -*-
import re


def validate_author_data(user_data):
    """Validate user data."""
    if not user_data:
        raise ValueError("The authors data must be provided!")
    if not isinstance(user_data, dict):
        raise ValueError("The author data must be a dictionary!")
    valid_keys = [
        "Name",
        "Email Address",
    ]
    for key in user_data.keys():
        if key not in valid_keys:
            print(key)
            raise ValueError(f"The only valid keys are {valid_keys}")
    if "Name" not in user_data.keys():
        raise ValueError("The First Name must be provided")
    if "Email Address" not in user_data.keys():
        raise ValueError("The Emai address must be provide!")
    if not user_data["Email Address"]:
        raise ValueError("The Email address must be provided!")
    if not user_data["Name"]:
        raise ValueError("The Name must be provided!")
    return True


def is_email_address_format_valid(email_address: str) -> bool:
    """Check that the email address format is valid."""
    if not email_address:
        raise ValueError("The email_address cannot be an empty value")

    if not isinstance(email_address, str):
        raise ValueError("The email_address must be a string")

    #  Regular expression for validating an Email
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if re.fullmatch(regex, email_address):
        return True
    return False
