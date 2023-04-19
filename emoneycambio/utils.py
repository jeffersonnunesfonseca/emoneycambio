import re
from unidecode import unidecode
from sqlalchemy import inspect

def only_numbers(string: str):
    return int(''.join(i for i in string if i.isdigit()))

def remove_accents_from_string(string: str):
    return unidecode(string)

def string_to_url(string: str):
    return string.replace(" ", "-")

def transform_sqlalchemy_row_in_object(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}