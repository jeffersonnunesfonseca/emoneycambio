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

def de_para_reasons(reason):

    de_para = {
        'pf-reason-1-send':  'Minha própria conta no exterior',
        'pf-reason-2-send':  'Familiar ou amigo',
        'pf-reason-3-send':  'Pagamento de um produto',
        'pf-reason-4-send':  'Pagamento de um serviço',
        'pf-reason-5-send':  'Investimento',
        'pf-reason-1-receive':  'Minha própria conta no brasil',
        'pf-reason-2-receive':  'Familiar ou amigo',
        'pf-reason-3-receive':  'Recebimento por produto vendido',
        'pf-reason-4-receive':  'Recebimento de serviços prestados',
        'pj-reason-1-send':  'Conta  da empresa no exterior',
        'pj-reason-2-send':  'Pagamento de um produto',
        'pj-reason-3-send':  'Pagamento de um serviço',
        'pj-reason-4-send':  'Investimento',
        'pj-reason-1-receive':  'Conta da empresa no brasil',
        'pj-reason-2-receive':  'Recebimento por produto vendido',
        'pj-reason-3-receive':  'Recebimento de serviços prestados'
    }
    try:
        return de_para[reason]
    except:
        return None