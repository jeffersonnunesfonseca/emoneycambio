from emoneycambio.resources.database import db
from emoneycambio import utils
from decimal import Decimal, ROUND_FLOOR

import json
import random

from sqlalchemy.sql import text
class Company:
    
    def __init__(self) -> None:
        self.db_session = db.session
    
    def get_companies_by_coin_and_location(self, url_coin: str, url_location: str):
        # return self._mock_filtered_companies()
        sql = f"""
            select 
                COALESCE((select value from configuration where `key` = 'iof_international_shipment_fee'), 0) as `default_configuration.international_shipment_iof_percentage`,
                COALESCE((select value from configuration where `key` = 'iof_tourism_fee'), 0) as `default_configuration.tourism_iof_percentage`,
                cb.url_location as `filters.city.url`, 
                cb.city as `filters.city.name`, 
                cb.uf as `filters.city.uf`,
                cbec.url_coin as `filters.coin.url`, 
                cbec.name as `filters.coin.name`,
                c.id as `companies.id`,
                cb.id as `companies.company_branch_id`,
                c.fantasy_name as `companies.name`,
                c.url as `companies.url`,
                c.logo_name as `companies.logo`,
                cb.site as `companies.site`,
                if(cbc.type!='EMAIL', cbc.value,null) as `companies.principal_phone.full_number`,
                if(cbc.type='WHATSAPP', 1,null) as `companies.principal_phone.is_whatsapp`,
                cbec.name as `companies.coin.name`,
                cbec.prefix as `companies.coin.prefix`,
                COALESCE(cbec.buy_tourism_vet, 0) as `companies.coin.buy_tourism_vet`,
                COALESCE(cbec.sell_tourism_vet, 0) as `companies.coin.sell_tourism_vet`,
                COALESCE(cbec.dispatch_international_shipment_vet, 0) as `companies.coin.dispatch_international_shipment_vet`,
                COALESCE(cbec.receipt_international_shipment_vet, 0) as `companies.coin.receipt_international_shipment_vet`,
                COALESCE(cbec.buy_tourism_exchange_fee, 0) as `companies.coin.buy_tourism_exchange_fee`,
                COALESCE(cbec.sell_tourism_exchange_fee, 0) as `companies.coin.sell_tourism_exchange_fee`,
                COALESCE(cbec.dispatch_international_shipment_exchange_fee, 0) as `companies.coin.dispatch_international_shipment_exchange_fee`,
                COALESCE(cbec.receipt_international_shipment_exchange_fee, 0) as `companies.coin.receipt_international_shipment_exchange_fee`,
                cbec.updated_at as `companies.coin.last_updated`,
                cbec.delivery as `companies.delivery.exists`,
                COALESCE(cbec.delivery_value, 0) as `companies.delivery.value`
            from company c
            inner join company_branch cb on cb.company_id = c.id
            inner join company_branch_exchange_coin cbec on cbec.company_branch_id = cb.id
            left join company_branch_contact cbc on cbc.company_branch_id = cb.id
            where 1=1
                and c.status = 'ENABLED'
                and cb.status = 'ENABLED' and cb.url_location = '{url_location}'
                and cbec.status ='ENABLED' and cbec.url_coin = '{url_coin}';

        """
        result_company = self.db_session.execute(text(sql)).fetchall()
        return_results = self._default_return_results_schema()
        return_results['companies'] = []
        
        if not result_company:
            return False
        
        
        for row in result_company:
            company_schema = self.company_schema()
            default_configuration_schema = self.default_configuration_schema()
            filters_schema = self.filters_schema()
            
            # pega as chaves que foram retorandas da querie e split pelo .
            for key in row._mapping.keys():
                keys_split = str(key).split(".")

                # apos o split a primeira posição sempre sera qual schema utilizar
                if keys_split[0] == "default_configuration":
                    schema = default_configuration_schema
                    
                elif keys_split[0] == "filters":
                    schema = filters_schema
                
                elif keys_split[0] == "companies":                       
                    schema = company_schema
                
                # macete para montar de forma dinamica o retorno esperado pelo front
                if len(keys_split) == 2:
                    schema[keys_split[1]] = row._mapping[key]
                    
                elif len(keys_split) == 3:
                    schema[keys_split[1]][keys_split[2]] = row._mapping[key]
                    
                elif len(keys_split) == 4:
                    schema[keys_split[1]][keys_split[2]][keys_split[3]] = row._mapping[key]    
            
            # ajuste para pegar logo 
            if 'logo' in company_schema:
                company_schema['logo'] = f"images/companies/{company_schema['url']}/{company_schema['logo']}"
            # mantem padrao no nome
            if 'name' in company_schema:
                company_schema['name'] = str(company_schema['name']).capitalize()
                
            company_schema['coin']['buy_tourism_vet'] = Decimal(company_schema['coin']['buy_tourism_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR) or 0
            company_schema['coin']['sell_tourism_vet'] = Decimal(company_schema['coin']['sell_tourism_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
            company_schema['coin']['dispatch_international_shipment_vet'] = Decimal(company_schema['coin']['dispatch_international_shipment_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
            company_schema['coin']['receipt_international_shipment_vet'] = Decimal(company_schema['coin']['receipt_international_shipment_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
            company_schema['coin']['buy_tourism_exchange_fee'] = Decimal(company_schema['coin']['buy_tourism_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
            company_schema['coin']['sell_tourism_exchange_fee'] = Decimal(company_schema['coin']['sell_tourism_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
            company_schema['coin']['dispatch_international_shipment_exchange_fee'] = Decimal(company_schema['coin']['dispatch_international_shipment_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
            company_schema['coin']['receipt_international_shipment_exchange_fee'] = Decimal(company_schema['coin']['receipt_international_shipment_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
            # monta retorno final 
            return_results['companies'].append(company_schema)
            return_results['default_configuration'] = default_configuration_schema
            return_results['filters'] = filters_schema
            
        return return_results

    def get_company_to_negotiation(self, **filters):

        AND_TYPE = " AND (cbec.sell_tourism_vet is not null or cbec.buy_tourism_vet is not null) " if filters['type'] == "papel-moeda" else ""
        AND_MODALITY = " AND cbec.sell_tourism_vet is not null " if filters["modality"] == "vender" else " AND cbec.buy_tourism_vet is not null "

        sql = f"""
            select COALESCE((select value from configuration where `key` = 'iof_international_shipment_fee'), 0) as `default_configuration.international_shipment_iof_percentage`,
                COALESCE((select value from configuration where `key` = 'iof_tourism_fee'), 0) as `default_configuration.tourism_iof_percentage`,
                cb.url_location as `filters.city.url`, 
                cb.city as `filters.city.name`, 
                cb.uf as `filters.city.uf`,
                cbec.url_coin as `filters.coin.url`, 
                cbec.name as `filters.coin.name`,
                c.id as `companies.id`,
                cb.id as `companies.company_branch_id`,
                c.fantasy_name as `companies.name`,
                c.url as `companies.url`,
                c.logo_name as `companies.logo`,
                cb.site as `companies.site`,
                if(cbc.type!='EMAIL', cbc.value,null) as `companies.principal_phone.full_number`,
                if(cbc.type='WHATSAPP', 1,null) as `companies.principal_phone.is_whatsapp`,
                cbec.name as `companies.coin.name`,
                cbec.prefix as `companies.coin.prefix`,
                COALESCE(cbec.buy_tourism_vet, 0) as `companies.coin.buy_tourism_vet`,
                COALESCE(cbec.sell_tourism_vet, 0) as `companies.coin.sell_tourism_vet`,
                COALESCE(cbec.dispatch_international_shipment_vet, 0) as `companies.coin.dispatch_international_shipment_vet`,
                COALESCE(cbec.receipt_international_shipment_vet, 0) as `companies.coin.receipt_international_shipment_vet`,
                COALESCE(cbec.buy_tourism_exchange_fee, 0) as `companies.coin.buy_tourism_exchange_fee`,
                COALESCE(cbec.sell_tourism_exchange_fee, 0) as `companies.coin.sell_tourism_exchange_fee`,
                COALESCE(cbec.dispatch_international_shipment_exchange_fee, 0) as `companies.coin.dispatch_international_shipment_exchange_fee`,
                COALESCE(cbec.receipt_international_shipment_exchange_fee, 0) as `companies.coin.receipt_international_shipment_exchange_fee`,
                cbec.updated_at as `companies.coin.last_updated`,
                cbec.delivery as `companies.delivery.exists`,
                COALESCE(cbec.delivery_value, 0) as `companies.delivery.value`
            from company c
            inner join company_branch cb on cb.company_id = c.id
            left join company_branch_contact cbc on cbc.company_branch_id = cb.id and cbc.status = 'ENABLED' and cbc.principal=1
            inner join company_branch_exchange_coin cbec on cbec.company_branch_id = cb.id
            where 1=1
                and c.status = 'ENABLED'
                
                {AND_MODALITY}
                {AND_TYPE}
                and cb.status = 'ENABLED' and cb.url_location = '{filters['location']}'
                and cbec.status ='ENABLED' and cbec.url_coin = '{filters['coin']}'
                and cb.id = {filters['companybranchid']}
        """

        row = self.db_session.execute(text(sql)).fetchone()
        return_results = self._default_return_results_schema()
        return_results['company'] = None
        if not row:
            return False
        company_schema = self.company_schema()
        
        company_schema["company_schema"] = None

        default_configuration_schema = self.default_configuration_schema()
        filters_schema = self.filters_schema()
        
        # pega as chaves que foram retorandas da querie e split pelo .
        for key in row._mapping.keys():
            keys_split = str(key).split(".")

            # apos o split a primeira posição sempre sera qual schema utilizar
            if keys_split[0] == "default_configuration":
                schema = default_configuration_schema
                
            elif keys_split[0] == "filters":
                schema = filters_schema
            
            elif keys_split[0] == "companies":                       
                schema = company_schema
            
            # macete para montar de forma dinamica o retorno esperado pelo front
            if len(keys_split) == 2:
                schema[keys_split[1]] = row._mapping[key]
                
            elif len(keys_split) == 3:
                schema[keys_split[1]][keys_split[2]] = row._mapping[key]
                
            elif len(keys_split) == 4:
                schema[keys_split[1]][keys_split[2]][keys_split[3]] = row._mapping[key]    
        
        # ajuste para pegar logo 
        if 'logo' in company_schema:
            company_schema['logo'] = f"images/companies/{company_schema['url']}/{company_schema['logo']}"
        # mantem padrao no nome
        if 'name' in company_schema:
            company_schema['name'] = str(company_schema['name']).capitalize()

        company_schema['coin']['buy_tourism_vet'] = Decimal(company_schema['coin']['buy_tourism_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR) or 0
        company_schema['coin']['sell_tourism_vet'] = Decimal(company_schema['coin']['sell_tourism_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['dispatch_international_shipment_vet'] = Decimal(company_schema['coin']['dispatch_international_shipment_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['receipt_international_shipment_vet'] = Decimal(company_schema['coin']['receipt_international_shipment_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['buy_tourism_exchange_fee'] = Decimal(company_schema['coin']['buy_tourism_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['sell_tourism_exchange_fee'] = Decimal(company_schema['coin']['sell_tourism_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['dispatch_international_shipment_exchange_fee'] = Decimal(company_schema['coin']['dispatch_international_shipment_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['receipt_international_shipment_exchange_fee'] = Decimal(company_schema['coin']['receipt_international_shipment_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)

        # monta retorno final 
        return_results['company']=company_schema
        return_results['default_configuration'] = default_configuration_schema

        filters_schema["modality"] = str(filters["modality"]).capitalize()
        filters_schema["type"] = filters["type"] 
        filters_schema["companybranchid"] = filters["companybranchid"]
        
        return_results['filters'] = filters_schema

        return return_results
        
    def get_allowed_company_international_shipment(self, url_coin: str = 'dolar-americano'):
        
        allowed_companies = self.db_session.execute(text("SELECT value FROM emoneycambio.configuration where `key` = 'allowed_companies_international_shipment'")).fetchone()        
        companies_url = list(filter(None, str(allowed_companies.value).split("|")))
        allowed_company = random.choice(companies_url)
        sql = f"""
            select 
                COALESCE((select value from configuration where `key` = 'iof_international_shipment_fee'), 0) as `default_configuration.international_shipment_iof_percentage`,
                COALESCE((select value from configuration where `key` = 'iof_tourism_fee'), 0) as `default_configuration.tourism_iof_percentage`,
                cb.url_location as `filters.city.url`, 
                cb.city as `filters.city.name`, 
                cb.uf as `filters.city.uf`,
                cbec.url_coin as `filters.coin.url`, 
                cbec.name as `filters.coin.name`,
                c.id as `companies.id`,
                cb.id as `companies.company_branch_id`,
                c.fantasy_name as `companies.name`,
                c.url as `companies.url`,
                c.logo_name as `companies.logo`,
                cb.site as `companies.site`,
                if(cbc.type!='EMAIL', cbc.value,null) as `companies.principal_phone.full_number`,
                if(cbc.type='WHATSAPP', 1,null) as `companies.principal_phone.is_whatsapp`,
                cbec.name as `companies.coin.name`,
                cbec.prefix as `companies.coin.prefix`,
                COALESCE(cbec.buy_tourism_vet, 0) as `companies.coin.buy_tourism_vet`,
                COALESCE(cbec.sell_tourism_vet, 0) as `companies.coin.sell_tourism_vet`,
                COALESCE(cbec.dispatch_international_shipment_vet, 0) as `companies.coin.dispatch_international_shipment_vet`,
                COALESCE(cbec.receipt_international_shipment_vet, 0) as `companies.coin.receipt_international_shipment_vet`,
                COALESCE(cbec.buy_tourism_exchange_fee, 0) as `companies.coin.buy_tourism_exchange_fee`,
                COALESCE(cbec.sell_tourism_exchange_fee, 0) as `companies.coin.sell_tourism_exchange_fee`,
                COALESCE(cbec.dispatch_international_shipment_exchange_fee, 0) as `companies.coin.dispatch_international_shipment_exchange_fee`,
                COALESCE(cbec.receipt_international_shipment_exchange_fee, 0) as `companies.coin.receipt_international_shipment_exchange_fee`,
                cbec.updated_at as `companies.coin.last_updated`,
                cbec.delivery as `companies.delivery.exists`,
                COALESCE(cbec.delivery_value, 0) as `companies.delivery.value`
            from company c
            inner join company_branch cb on cb.company_id = c.id
            inner join company_branch_exchange_coin cbec on cbec.company_branch_id = cb.id
            left join company_branch_contact cbc on cbc.company_branch_id = cb.id and cbc.status = 'ENABLED' and cbc.principal=1 
            where 1=1
                and c.status = 'ENABLED' and c.url= '{allowed_company}'
                and (cbec.dispatch_international_shipment_vet is not null or cbec.receipt_international_shipment_vet is not null)
                and cbec.url_coin = '{url_coin}'
        """
        
        row = self.db_session.execute(text(sql)).fetchone()
        return_results = self._default_return_results_schema()
        return_results['company'] = None
        if not row:
            return False
        
        company_schema = self.company_schema()        
        default_configuration_schema = self.default_configuration_schema()
        filters_schema = self.filters_schema()

        # pega as chaves que foram retorandas da querie e split pelo .
        # import ipdb; ipdb.set_trace()
        for key in row._mapping.keys():
            keys_split = str(key).split(".")

            # apos o split a primeira posição sempre sera qual schema utilizar
            if keys_split[0] == "default_configuration":
                schema = default_configuration_schema
                
            elif keys_split[0] == "filters":
                schema = filters_schema
            
            elif keys_split[0] == "companies":                       
                schema = company_schema
            
            # macete para montar de forma dinamica o retorno esperado pelo front
            if len(keys_split) == 2:
                schema[keys_split[1]] = row._mapping[key]
                
            elif len(keys_split) == 3:
                schema[keys_split[1]][keys_split[2]] = row._mapping[key]
                
            elif len(keys_split) == 4:
                schema[keys_split[1]][keys_split[2]][keys_split[3]] = row._mapping[key]    
        
        # ajuste para pegar logo 
        if 'logo' in company_schema:
            company_schema['logo'] = f"images/companies/{company_schema['url']}/{company_schema['logo']}"
        # mantem padrao no nome
        if 'name' in company_schema:
            company_schema['name'] = str(company_schema['name']).capitalize()
            
        company_schema['coin']['buy_tourism_vet'] = Decimal(company_schema['coin']['buy_tourism_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR) or 0
        company_schema['coin']['sell_tourism_vet'] = Decimal(company_schema['coin']['sell_tourism_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['dispatch_international_shipment_vet'] = Decimal(company_schema['coin']['dispatch_international_shipment_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['receipt_international_shipment_vet'] = Decimal(company_schema['coin']['receipt_international_shipment_vet']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['buy_tourism_exchange_fee'] = Decimal(company_schema['coin']['buy_tourism_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['sell_tourism_exchange_fee'] = Decimal(company_schema['coin']['sell_tourism_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['dispatch_international_shipment_exchange_fee'] = Decimal(company_schema['coin']['dispatch_international_shipment_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        company_schema['coin']['receipt_international_shipment_exchange_fee'] = Decimal(company_schema['coin']['receipt_international_shipment_exchange_fee']).quantize(Decimal('.01'), rounding=ROUND_FLOOR)
        # monta retorno final 
        return_results['company']=company_schema
        return_results['filters'] = filters_schema
        return_results['default_configuration'] = default_configuration_schema
        return return_results
        # return self._mock_get_allowed_company_international_shipment()
    
    
        data = {
                "default_configuration": {                
                    "tourism_iof_percentage": 0.01100,
                    "international_shipment_iof_percentage": 0.03800,
                    "default_utc_datetime": 0
                },
                "company": {
                    "id": 2,
                    "name": "Get Money Câmbio",
                    "url": "get-money-cambio",
                    "logo": "images/companies/get-money-cambio/logo-get-money-cambio.png",
                    "site": "https://www.getmoney.com.br/",
                    "principal_phone": {
                        "ddi": "55",
                        "ddd": "11",
                        "number": "30181880",
                        "full_number": "551130181880",
                        "is_whatsapp": True
                    },
                    "coin": {
                        "name": "Dólar americano",
                        "prefix": "US$",
                        "buy_tourism_vet": 5.28000,
                        "sell_tourism_vet": 4.99000,
                        "dispatch_international_shipment_vet": 5.16000,   
                        "receipt_international_shipment_vet": 4.94000,
                        "buy_tourism_fee": 5.28000,
                        "sell_tourism_fee": 4.99000,
                        "dispatch_international_shipment_fee": 5.16000,   
                        "receipt_international_shipment_fee": 4.94000,
                        "last_updated": "2023-04-07T20:00:00"
                    },
                    "delivery": {
                        "exists": False,
                        "fee": None
                    }
                }
            }
        return data

    def _default_return_results_schema(self):
        return_results = {
            
            'default_configuration': None,
            'filters': None,
            'companies': None
        }
        
        return return_results
    
    def filters_schema(self):
        
        filters_schema = {
            "city": {
                "url": None,
                "name": None,
                "uf": None
            },
            "coin": {
                "url": None,
                "name": None
            }
        }
        
        return filters_schema
    
    def default_configuration_schema(self):
        default_configuration_schema = {
            "tourism_iof_percentage": None,
            "international_shipment_iof_percentage": None
        }
        
        return default_configuration_schema
    
    def company_schema(self):
        
        company_schema = {
            "id": None,
            "name": None,
            "url": None,
            "logo": None,
            "site": None,
            "principal_phone": {
                "full_number": None,
                "is_whatsapp": None
            },
            "coin": {
                    "name": None,
                    "prefix": None,
                    "buy_tourism_vet": None,
                    "sell_tourism_vet": None,
                    "dispatch_international_shipment_vet": None,   
                    "receipt_international_shipment_vet": None,
                    "buy_tourism_fee": None,
                    "sell_tourism_fee": None,
                    "dispatch_international_shipment_fee": None,   
                    "receipt_international_shipment_fee": None,                            
                    "last_updated": None
            },
            "delivery": {
                "exists": None,
                "value": None
            }
        }
        
        return company_schema