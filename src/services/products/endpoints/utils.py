# src/services/products/endpoints/utils.py
import re

"""This package contains usefully functions and methods """

def validate_password(plain_password: str) -> tuple[bool, str]:
    """
    This function is used to validate the password entered by the user.
    the validation is True if
        1. the length of the plain_password is >= 8
        2. plain_password contains at least 1 uppercase letter
        3. plain_password contains at least 1 lowercase letter
        4. plain_password contains at least 1 digit
        5. plain_password contains at least symbol such as [., @, #, _, -, +, *]
    """
    # 1. validation of length
    if len(plain_password) < 8:
        message = "Password must be at least 8 characters long"
        return False, message

    # 2. validation of uppercase letter
    capital_letter = re.findall(r"[A-Z]", plain_password)
    if len(capital_letter) < 1:
        message = "Password must contain at least 1 capital letter"
        return False, message
    # 3. validation of lowercase letter
    lowercase_letter = re.findall(r"[a-z]", plain_password)
    if len(lowercase_letter) < 1:
        message = "Password must contain at least 1 lowercase letter"
        return False, message
    # 4. validation of digit
    digit = re.findall(r"[0-9]", plain_password)
    if len(digit) < 1:
        message = "Password must contain at least 1 digit"
        return False, message
    # 5. validation of a symbol
    valid_symbols = r"[@#_\-+\*\.]"
    symbol = re.findall(valid_symbols, plain_password)
    if len(symbol) < 1:
        message = "Password must contain at least 1 special character such as . @ # _ - + *"
        return False, message

    message = "correct password format"
    return True, message

