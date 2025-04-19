import re

def is_valid_israeli_id(id_str):
    """
    Validates an Israeli ID number using the checksum and Luhn algorithm.

    An Israeli ID must:
    - Contain exactly 9 digits
    - Pass a checksum calculation based on alternating multipliers 

    Args:
        id_str (str): The ID number as a string.

    Returns:
        bool: True if the ID is valid, False otherwise.
    """
    if not id_str.isdigit() or len(id_str) != 9:
        return False

    total = 0
    for i, digit in enumerate(id_str):
        num = int(digit) * (i % 2 + 1) # Multiplier alternates between 1 and 2
        if num > 9:
            num -= 9 # Subtract 9 if the result is greater than 9 (digit sum)
        total += num

    return total % 10 == 0

def is_valid_phone(phone_num):
    """
    Validates an Israeli mobile phone number using regex.

    Israeli numbers must:
    - Start with 050, 051, 052, 053, 054, 055, or 058
    - Be exactly 10 digits long

    Args:
        phone_num (str): The phone number as a string.

    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    return re.fullmatch(r'^05[0123458]\d{7}$', phone_num) is not None
