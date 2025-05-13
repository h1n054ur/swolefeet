import re

def is_valid_phone_number(number):
    return bool(re.match(r"^\+\d{10,15}$", number))

def is_valid_url(url):
    return bool(re.match(r"^https?://", url))

def is_valid_country_code(code):
    return bool(re.match(r"^[A-Z]{2}$", code))

def is_valid_capability_list(capabilities):
    allowed = {"SMS", "MMS", "VOICE"}
    return all(cap.upper() in allowed for cap in capabilities)
