import re

def is_valid_israeli_id(id_str):
    if not id_str.isdigit() or len(id_str) != 9:
        return False

    total = 0
    for i, digit in enumerate(id_str):
        num = int(digit) * (i % 2 + 1)
        if num > 9:
            num -= 9
        total += num

    return total % 10 == 0

def is_valid_phone(phone_num):
    return re.fullmatch(r'^05[0123458]\d{7}$', phone_num) is not None
