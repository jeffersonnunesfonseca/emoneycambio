import re
from unidecode import unidecode
from sqlalchemy import inspect

def only_numbers(string: str):
    if not string:
        return None
    
    return int(''.join(i for i in string if i.isdigit()))

def remove_accents_from_string(string: str):
    return unidecode(string)

def string_to_url(string: str):
    string = remove_accents_from_string(string)
    return string.replace(" ", "-").lower()

def transform_sqlalchemy_row_in_object(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}