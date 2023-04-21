import fire
import logging
import requests
import json
import re
from datetime import datetime
from sqlalchemy import exc
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from emoneycambio.app import app
from emoneycambio import utils
from emoneycambio.services.company_branch import CompanyBranch
from emoneycambio.services.exchange_company_branch_coin import CompanyBranchExchangeCoin
from emoneycambio.services.exchange_commercial_coin import ExchangeCommercialCoin
from emoneycambio.resources.database import db
from emoneycambio.models.models import ExchangeCommercialCoinModel, ExchangeCommercialCoinHistoryModel


LOGGER = logging.getLogger(__name__)
def update_exchange_commercial_coin():
    response = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL,CAD-BRL,GBP-BRL')
    response.raise_for_status()
    data = response.json()
    
    for key, value in data.items():
        name = str(value["name"]).replace("/Real Brasileiro", "")
        value = value["bid"]
        with app.app_context() as apps:
            exchange_commercial_coin = ExchangeCommercialCoinModel()
            coin = ExchangeCommercialCoinModel.query.filter_by(key=key).first()
            if coin:
                exchange_commercial_coin = coin
            else:                
                exchange_commercial_coin.name = name
                exchange_commercial_coin.key = key
                exchange_commercial_coin.prefix = value['code']
                
            exchange_commercial_coin.url = utils.string_to_url(name)
            exchange_commercial_coin.value = value
            exchange_commercial_coin.updated_at = datetime.utcnow()
            try:                
                exchange_commercial_coin_history = ExchangeCommercialCoinHistoryModel()
                exchange_commercial_coin_history.exchange_commercial_coin_id = exchange_commercial_coin.id
                exchange_commercial_coin_history.value = value
                            
                db.session.add(exchange_commercial_coin)
            
                db.session.add(exchange_commercial_coin_history)
                db.session.commit()
                
            except exc.IntegrityError as ex:
                LOGGER.error(str(ex))   
                
                if "Duplicate" in str(ex):
                    continue
                
                return False    
                
            finally:
                db.session.flush()
  
def get_coins_get_money_corretora():
    LOGGER.info("buscando dados no site")
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('--ignore-certificate-errors')   
    driver = webdriver.Remote(options=webdriver_options, command_executor="http://127.0.0.1:4444/wd/hub")           
    session = driver.get("https://getmoney.com.br/")
    result = driver.execute_script("return window['loja1']")
    driver.quit()
    
    coins = result['moedas']
    
    remessa_coins = []
    turismo_coins = []
    shoppings = []
    
    shoppings_de_para = {
        "shopping-patio-paulista": {"location_url": "sao-paulo-sp", "city": "São Paulo", "uf": "SP"},
        "shopping-eldorado": {"location_url": "sao-paulo-sp", "city": "São Paulo", "uf": "SP"},
        "shopping-rio-design" : {"location_url": "rio-de-janeiro-rj", "city": "Rio de Janeiro", "uf": "RJ"},
    }
    
    for moeda in coins:
        if moeda["indisponivel"] != "False":
            continue
        
        if int(moeda["idTipoItemVitrine"]) in (1, 2) and int(moeda["idTipoMoeda"]) == 1:
            turismo_coins.append(moeda)
            shoppings.append(moeda['descricaoPraca'])
        elif int(moeda["idTipoItemVitrine"]) in (3, 4) and int(moeda["idPraca"]) == 0:
            remessa_coins.append(moeda)
            shoppings.append(moeda['descricaoPraca'])
    
    total_turismo = len(turismo_coins)
    total_remessa = len(remessa_coins)
    LOGGER.info(f"{total_turismo} moedas turismo")
    LOGGER.info(f"{total_remessa} moedas remessa_coins")
    
    with app.app_context() as apps:
        company_key = "get-money-cambio"
        site = "https://getmoney.com.br/"
        
        company_branch = CompanyBranch()
        cont = 0
        if turismo_coins:
            for turismo_coin in turismo_coins:
                cont +=1

                if not turismo_coin['taxa']:
                    continue

                location = shoppings_de_para[utils.string_to_url(turismo_coin['descricaoPraca'])] if turismo_coin['descricaoPraca'] else {"location_url": "sao-paulo-sp", "city": "São Paulo", "uf": "SP"}
                current_company_branch = company_branch.get_company_branch_by_company_url_and_url_location(company_key, location['location_url'])
                if not current_company_branch.original_company_id:
                    LOGGER.info(f"empresa nao existe do nosso lado {company_key}")
                    continue
   
                data = {
                    "company_id": current_company_branch.original_company_id,
                    "principal": current_company_branch.principal if current_company_branch.company_branch_id else 0,
                    "name": current_company_branch.name,
                    "site": site,
                    "full_address": None,
                    "complement": turismo_coin['descricaoPraca'] if turismo_coin['descricaoPraca'] else None,
                    "uf": location['uf'],
                    "city": location['city'],
                    "cep": None,
                    "lat": None,
                    "lng": None
                }
                
                LOGGER.info(f"{cont} de {total_turismo} - turismo - criando company_branch {data}")
                new_company_branch_id = company_branch.create_company_branch(**data)
                LOGGER.info(f"{cont} de {total_turismo} - turismo - company_branch criada {new_company_branch_id}")
                if not new_company_branch_id:
                    continue
                
                data = {
                    "company_branch_id": new_company_branch_id,
                    "name": "Dólar americano" if turismo_coin['nome'] == "Dólar" else str(turismo_coin['nome']).capitalize(),
                    "prefix": str(turismo_coin['sigla']).upper(),
                    "buy_tourism_vet": turismo_coin['taxa'] if int(turismo_coin['idTipoItemVitrine']) == 1 else None,
                    "sell_tourism_vet": turismo_coin['taxa'] if int(turismo_coin['idTipoItemVitrine']) ==2 else None,
                    "dispatch_international_shipment_vet": turismo_coin['taxa'] if int(turismo_coin['idTipoItemVitrine']) == 3 else None,
                    "receipt_international_shipment_vet": turismo_coin['taxa'] if int(turismo_coin['idTipoItemVitrine']) == 4 else None,
                    "delivery": False,
                    "delivery_value": None
                }

                LOGGER.info(f"{cont} de {total_turismo} - turismo - criando create_company_branch_exchange_coin {data}")
                action = CompanyBranchExchangeCoin()        
                id = action.create_company_branch_exchange_coin(**data)
                LOGGER.info(f"{cont} de {total_turismo} - turismo - create_company_branch_exchange_coin criada {id}")

            #FORCE RJ pois as mesmas moedas tbm existem la
            cont = 0
            for turismo_coin in turismo_coins:
                cont +=1
                if not turismo_coin['taxa']:
                    continue

                location = shoppings_de_para['shopping-rio-design']
                current_company_branch = company_branch.get_company_branch_by_company_url_and_url_location(company_key, location['location_url'])
                if not current_company_branch.original_company_id:
                    LOGGER.info(f"empresa nao existe do nosso lado {company_key}")
                    continue
   
                data = {
                    "company_id": current_company_branch.original_company_id,
                    "principal": current_company_branch.principal if current_company_branch.company_branch_id else 0,
                    "name": current_company_branch.name,
                    "site": site,
                    "full_address": None,
                    "complement": turismo_coin['descricaoPraca'] if turismo_coin['descricaoPraca'] else None,
                    "uf": location['uf'],
                    "city": location['city'],
                    "cep": None,
                    "lat": None,
                    "lng": None
                }
                
                LOGGER.info(f"{cont} de {total_turismo} - turismo - criando company_branch {data}")
                new_company_branch_id = company_branch.create_company_branch(**data)
                LOGGER.info(f"{cont} de {total_turismo} - turismo - company_branch criada {new_company_branch_id}")
                if not new_company_branch_id:
                    continue
                
                data = {
                    "company_branch_id": new_company_branch_id,
                    "name": "Dólar americano" if turismo_coin['nome'] == "Dólar" else str(turismo_coin['nome']).capitalize(),
                    "prefix": str(turismo_coin['sigla']).upper(),
                    "buy_tourism_vet": turismo_coin['taxa'] if int(turismo_coin['idTipoItemVitrine']) == 1 else None,
                    "sell_tourism_vet": turismo_coin['taxa'] if int(turismo_coin['idTipoItemVitrine']) ==2 else None,
                    "dispatch_international_shipment_vet": turismo_coin['taxa'] if int(turismo_coin['idTipoItemVitrine']) == 3 else None,
                    "receipt_international_shipment_vet": turismo_coin['taxa'] if int(turismo_coin['idTipoItemVitrine']) == 4 else None,
                    "delivery": False,
                    "delivery_value": None
                }

                LOGGER.info(f"{cont} de {total_turismo} - turismo - criando create_company_branch_exchange_coin {data}")
                action = CompanyBranchExchangeCoin()        
                id = action.create_company_branch_exchange_coin(**data)
                LOGGER.info(f"{cont} de {total_turismo} - turismo - create_company_branch_exchange_coin criada {id}")
        cont = 0                                
        if remessa_coins:
            for remessa_coin in remessa_coins:
                cont +=1
                if not remessa_coin['taxa']:
                    continue

                location = shoppings_de_para[utils.string_to_url(remessa_coin['descricaoPraca'])] if remessa_coin['descricaoPraca'] else {"location_url": "sao-paulo-sp", "city": "São Paulo", "uf": "SP"}
                current_company_branch = company_branch.get_company_branch_by_company_url_and_url_location(company_key, location['location_url'])
                if not current_company_branch.original_company_id:
                    LOGGER.info(f"empresa nao existe do nosso lado {company_key}")
                    continue
   
                data = {
                    "company_id": current_company_branch.original_company_id,
                    "principal": current_company_branch.principal if current_company_branch.company_branch_id else 0,
                    "name": current_company_branch.name,
                    "site": site,
                    "full_address": None,
                    "complement": remessa_coin['descricaoPraca'] if remessa_coin['descricaoPraca'] else None,
                    "uf": location['uf'],
                    "city": location['city'],
                    "cep": None,
                    "lat": None,
                    "lng": None
                }
                
                LOGGER.info(f"{cont} de {total_remessa} - remessa - criando company_branch {data}")
                new_company_branch_id = company_branch.create_company_branch(**data)
                LOGGER.info(f"{cont} de {total_remessa} - remessa - company_branch criada {new_company_branch_id}")

                
                data = {
                    "company_branch_id": new_company_branch_id,
                    "name": "Dólar americano" if remessa_coin['nome'] == "Dólar" else str(remessa_coin['nome']).capitalize(),
                    "prefix": str(remessa_coin['sigla']).upper(),
                    "buy_tourism_vet": remessa_coin['taxa'] if int(remessa_coin['idTipoItemVitrine']) == 1 else None,
                    "sell_tourism_vet": remessa_coin['taxa'] if int(remessa_coin['idTipoItemVitrine']) ==2 else None,
                    "dispatch_international_shipment_vet": remessa_coin['taxa'] if int(remessa_coin['idTipoItemVitrine']) == 3 else None,
                    "receipt_international_shipment_vet": remessa_coin['taxa'] if int(remessa_coin['idTipoItemVitrine']) == 4 else None,
                    "delivery": False,
                    "delivery_value": None
                }

                LOGGER.info(f"{cont} de {total_remessa} - turismo - criando create_company_branch_exchange_coin {data}")
                action = CompanyBranchExchangeCoin()        
                id = action.create_company_branch_exchange_coin(**data)
                LOGGER.info(f"{cont} de {total_remessa} - turismo - create_company_branch_exchange_coin criada {id}")
            
            #FORCE RJ pois as mesmas moedas tbm existem la
            for remessa_coin in remessa_coins:
                cont +=1

                if not remessa_coin['taxa']:
                    continue

                location = shoppings_de_para['shopping-rio-design']
                current_company_branch = company_branch.get_company_branch_by_company_url_and_url_location(company_key, location['location_url'])
                if not current_company_branch.original_company_id:
                    LOGGER.info(f"empresa nao existe do nosso lado {company_key}")
                    continue

                data = {
                    "company_id": current_company_branch.original_company_id,
                    "principal": current_company_branch.principal if current_company_branch.company_branch_id else 0,
                    "name": current_company_branch.name,
                    "site": site,
                    "full_address": None,
                    "complement": remessa_coin['descricaoPraca'] if remessa_coin['descricaoPraca'] else None,
                    "uf": location['uf'],
                    "city": location['city'],
                    "cep": None,
                    "lat": None,
                    "lng": None
                }
                
                LOGGER.info(f"{cont} de {total_remessa} - remessa - criando company_branch {data}")
                new_company_branch_id = company_branch.create_company_branch(**data)
                LOGGER.info(f"{cont} de {total_remessa} - remessa - company_branch criada {new_company_branch_id}")

                
                data = {
                    "company_branch_id": new_company_branch_id,
                    "name": "Dólar americano" if remessa_coin['nome'] == "Dólar" else str(remessa_coin['nome']).capitalize(),
                    "prefix": str(remessa_coin['sigla']).upper(),
                    "buy_tourism_vet": remessa_coin['taxa'] if int(remessa_coin['idTipoItemVitrine']) == 1 else None,
                    "sell_tourism_vet": remessa_coin['taxa'] if int(remessa_coin['idTipoItemVitrine']) ==2 else None,
                    "dispatch_international_shipment_vet": remessa_coin['taxa'] if int(remessa_coin['idTipoItemVitrine']) == 3 else None,
                    "receipt_international_shipment_vet": remessa_coin['taxa'] if int(remessa_coin['idTipoItemVitrine']) == 4 else None,
                    "delivery": False,
                    "delivery_value": None
                }

                LOGGER.info(f"{cont} de {total_remessa} - turismo - criando create_company_branch_exchange_coin {data}")
                action = CompanyBranchExchangeCoin()        
                id = action.create_company_branch_exchange_coin(**data)
                LOGGER.info(f"{cont} de {total_remessa} - turismo - create_company_branch_exchange_coin criada {id}")

def get_coins_frente_corretora():
    
    company_key = "frente-corretora"
    site = "https://frentecorretora.com.br/"
    
    with app.app_context() as apps:
        # busca moedas que estamos trabalhando, basta cadastra-las na tabela exchange_commercial_coin
        exchange_commercial_coin = ExchangeCommercialCoin()
        coins = exchange_commercial_coin.get_updated_coins()
        company_branch = CompanyBranch()
        
        locations = [
            {
                
                "city": "Curitiba",
                "uf": "PR",
                "url": "curitiba-pr",
                "tourism_location": "WL-FRENTE-CTB"
            },
            {
                
                "city": "Rio de Janeiro",
                "uf": "RJ",
                "url": "rio-de-janeiro-rj",
                "tourism_location": "WL-FRENTE-CTB"
            },
            {
                
                "city": "São Paulo",
                "uf": "SP",
                "url": "sao-paulo-sp",
                "tourism_location": "WL-FRENTE-CTB"
            }
        ]
        for location in locations:
            current_company_branch = company_branch.get_company_branch_by_company_url_and_url_location(company_key, location['url'])
            if not current_company_branch.original_company_id:
                LOGGER.info(f"empresa nao existe do nosso lado {company_key}")
                continue
            
            data = {
                "company_id": current_company_branch.original_company_id,
                "principal": current_company_branch.principal if current_company_branch.company_branch_id else 0,
                "name": current_company_branch.name,
                "site": site,
                "full_address": None,
                "complement": None,
                "uf": location['uf'],
                "city": location['city'],
                "cep": None,
                "lat": None,
                "lng": None
            }
            
            new_company_branch_id = company_branch.create_company_branch(**data)
            if not new_company_branch_id:
                continue    
            
            # aqui corre para buscar as moedas
            for coin in coins:
               
                try: 
                        LOGGER.info(f"buscando compra turismo {location['tourism_location']} - {coin['prefix']}")
                        response_tourism = requests.get(f'https://api.frentecorretora.com.br/v1/exchanges/paper-money/quotations/{location["tourism_location"]}?currency={coin["prefix"]}&value=100000&reverse=false')
                        response_tourism.raise_for_status()
                        data_tourism = response_tourism.json()
                        
                        LOGGER.info(f"buscando compra remessa envio {coin['prefix']}")
                        response_dispatch_international_shipment = requests.get(f'https://api.frentecorretora.com.br/v1/exchanges/remittance/outbound/reverse?purposeCode=AVAILABILITY&currency={coin["prefix"]}&correspondentId=1&value=120000')
                        response_dispatch_international_shipment.raise_for_status()
                        data_dispatch_international_shipment = response_dispatch_international_shipment.json()
                        
                        LOGGER.info(f"buscando compra remessa recebimento {coin['prefix']}")
                        response_receipt_international_shipment = requests.get(f'https://api.frentecorretora.com.br/v1/exchanges/remittance/inbound/reverse?purposeCode=AVAILABILITY&currency={coin["prefix"]}&correspondentId=1&value=120000')
                        response_receipt_international_shipment.raise_for_status()
                        data_receipt_international_shipment = response_receipt_international_shipment.json()
                except requests.exceptions.HTTPError as ex: 
                    if '404' in str(ex):
                        LOGGER.info(f"moeda nao encontrada {coin['prefix']}")
                        continue
                   
                
                data = {
                    
                    "company_branch_id": new_company_branch_id,
                    "name": data_tourism['currency']['name'],
                    "prefix": str(data_tourism['currency']['code']).upper(),
                    "buy_tourism_vet": float(data_tourism['total']['withTax']['value'])/10000,
                    "sell_tourism_vet": None,
                    "dispatch_international_shipment_vet": float(data_dispatch_international_shipment['currency']['price']['withTax']['value'])/10000,
                    "receipt_international_shipment_vet": float(data_receipt_international_shipment['currency']['price']['withTax']['value'])/10000,
                    "delivery": False,
                    "delivery_value": None
                }

                action = CompanyBranchExchangeCoin()        
                id = action.create_company_branch_exchange_coin(**data)

def get_coins_daycambio():
    
    company_key = "daycambio"
    site = "https://daycambio.com.br/"
    
    with app.app_context() as apps:
        # busca moedas que estamos trabalhando, basta cadastra-las na tabela exchange_commercial_coin
        exchange_commercial_coin = ExchangeCommercialCoin()
        coins = exchange_commercial_coin.get_updated_coins()
        company_branch = CompanyBranch()
        
        locations = [
            {
                
                "city": "Curitiba",
                "uf": "PR",
                "url": "curitiba-pr",
                "tourism_location": "WL-FRENTE-CTB"
            },
            {
                
                "city": "Rio de Janeiro",
                "uf": "RJ",
                "url": "rio-de-janeiro-rj",
                "tourism_location": "WL-FRENTE-CTB"
            },
            {
                
                "city": "São Paulo",
                "uf": "SP",
                "url": "sao-paulo-sp",
                "tourism_location": "WL-FRENTE-CTB"
            }
        ]
        for location in locations:
            current_company_branch = company_branch.get_company_branch_by_company_url_and_url_location(company_key, location['url'])
            if not current_company_branch.original_company_id:
                LOGGER.info(f"empresa nao existe do nosso lado {company_key}")
                continue
            
            data = {
                "company_id": current_company_branch.original_company_id,
                "principal": current_company_branch.principal if current_company_branch.company_branch_id else 0,
                "name": current_company_branch.name,
                "site": site,
                "full_address": None,
                "complement": None,
                "uf": location['uf'],
                "city": location['city'],
                "cep": None,
                "lat": None,
                "lng": None
            }
            
            new_company_branch_id = company_branch.create_company_branch(**data)
            if not new_company_branch_id:
                continue    
            
            # aqui corre para buscar as moedas
            for coin in coins:
               
                try: 
                        LOGGER.info(f"buscando compra turismo {location['tourism_location']} - {coin['prefix']}")
                        response_tourism = requests.get(f'https://api.frentecorretora.com.br/v1/exchanges/paper-money/quotations/{location["tourism_location"]}?currency={coin["prefix"]}&value=100000&reverse=false')
                        response_tourism.raise_for_status()
                        data_tourism = response_tourism.json()
                        
                        LOGGER.info(f"buscando compra remessa envio {coin['prefix']}")
                        response_dispatch_international_shipment = requests.get(f'https://api.frentecorretora.com.br/v1/exchanges/remittance/outbound/reverse?purposeCode=AVAILABILITY&currency={coin["prefix"]}&correspondentId=1&value=120000')
                        response_dispatch_international_shipment.raise_for_status()
                        data_dispatch_international_shipment = response_dispatch_international_shipment.json()
                        
                        LOGGER.info(f"buscando compra remessa recebimento {coin['prefix']}")
                        response_receipt_international_shipment = requests.get(f'https://api.frentecorretora.com.br/v1/exchanges/remittance/inbound/reverse?purposeCode=AVAILABILITY&currency={coin["prefix"]}&correspondentId=1&value=120000')
                        response_receipt_international_shipment.raise_for_status()
                        data_receipt_international_shipment = response_receipt_international_shipment.json()
                except requests.exceptions.HTTPError as ex: 
                    if '404' in str(ex):
                        LOGGER.info(f"moeda nao encontrada {coin['prefix']}")
                        continue
                   
                
                data = {
                    
                    "company_branch_id": new_company_branch_id,
                    "name": data_tourism['currency']['name'],
                    "prefix": str(data_tourism['currency']['code']).upper(),
                    "buy_tourism_vet": float(data_tourism['total']['withTax']['value'])/10000,
                    "sell_tourism_vet": None,
                    "dispatch_international_shipment_vet": float(data_dispatch_international_shipment['currency']['price']['withTax']['value'])/10000,
                    "receipt_international_shipment_vet": float(data_receipt_international_shipment['currency']['price']['withTax']['value'])/10000,
                    "delivery": False,
                    "delivery_value": None
                }

                action = CompanyBranchExchangeCoin()        
                id = action.create_company_branch_exchange_coin(**data)

if __name__ == "__main__":
    fire.Fire()