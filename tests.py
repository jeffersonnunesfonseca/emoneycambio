import logging
import sys
from emoneycambio.app import app

console = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s', level=logging.DEBUG, handlers=[console])

def test_get_companies_by_coin_and_location():
    with app.app_context():    
        from emoneycambio.services.company import Company
        action = Company()
        action.get_companies_by_coin_and_location("dolar-americano", "sao-paulo-sp")

def test_get_company_to_negotiation():
    with app.app_context():    
        from emoneycambio.services.company import Company
        action = Company()
        filters = {'modality': 'vender', 'type': 'papel-moeda', 'coin': 'dolar-americano', 'location': 'sao-paulo-sp', 'companyid': '2'}
        action.get_company_to_negotiation(**filters)
        
def test_get_allowed_company_international_shipment():
    with app.app_context():    
        from emoneycambio.services.company import Company
        action = Company()        
        action.get_allowed_company_international_shipment()

def test_create_exchange_proposal():
    with app.app_context():    
        from emoneycambio.services.exchange_proposal import ExchangeProposal
        action = ExchangeProposal()        
        data = {
            'company_branch_id': 1,
            'person_type': 'PF',
            'transaction_type': 'BUY',
            'exchange_type': 'TOURISM',
            'reason': None,
            'total_value': '211212',
            'iof_fee': '50934',
            'vet': '50934',
            'coin_name': 'Dólar americano',
            'document': '42192090854',
            'name': 'Jefferson Nunes',
            'responsible_name': None,
            'email': 'jeffersonnunesfonseca@gmail.com',
            'phone': '5541997439582',
            'phone_is_whatsapp': True,
            'delivery': 0,
            'ip': '164.163.46.22',
            'user_agent': "Mozilla/5.0 (Linux; Android 9; ASUS_X01BDA) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
            'headers': {'Host': 'localhost:5656', 'Connection': 'keep-alive', 'Sec-Ch-Ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Linux"', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Referer': 'http://localhost:5656/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7', 'Cookie': '_ga=GA1.1.2146253050.1680956824'}
        }
        
        action.create_exchange_proposal(**data)

def test_get_updated_coins():
    with app.app_context():    
        from emoneycambio.services.exchange_commercial_coin import ExchangeCommercialCoin
        action = ExchangeCommercialCoin()        
        action.get_updated_coins()


if __name__ == '__main__':
    # test_get_companies_by_coin_and_location()    
    # test_get_company_to_negotiation()
    # test_get_allowed_company_international_shipment()
    # test_create_exchange_proposal()
    test_get_updated_coins()