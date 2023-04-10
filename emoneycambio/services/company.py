# companies
class Company:
    
    def __init__(self) -> None:
        pass
    
    def get_companies_by_coin_and_location(self, coin, company):
        return self._mock_filtered_companies()
    
    def get_company_to_negotiation(self, **filters):
        # print(filters)
        return self._mock_get_company_to_negotiation(filters)
    
    def _mock_filtered_companies(self):
        
        response = {
            
            "default_configuration": {                
                "tourism_iof_percentage": 0.01100,
                "international_shipment_iof_percentage": 0.03800,
                "default_utc_datetime": 0
            },
            "filters":{
                "city": {
                    "url": "sao-paulo-sp",
                    "name": "São Paulo",
                    "uf": "SP"
                },
                "coin": {
                    "url": "dolar",
                    "name": "Dólar Americano"
                }
            },
            "companies": [
                {
                    "id": 1,
                    "name": "Frente Corretora",
                    "url": "frente-corretora",
                    "logo": "images/companies/frente-corretora/logo-frente-corretora.png",
                    "site": "https://frentecorretora.com.br/",
                    "principal_phone": {
                        "ddi": "55",
                        "ddd": "11",
                        "number": "42000850",
                        "full_number": "551142000850",
                        "is_whatsapp": True
                    },
                    "coin": {
                            "name": "Dólar americano",
                            "prefix": "US$",
                            "buy_tourism_vet": 5.32720,
                            "sell_tourism_vet": None,
                            "dispatch_international_shipment_vet": 5.18350,   
                            "receipt_international_shipment_vet": 4.43410,
                            "buy_tourism_fee": 5.32720,
                            "sell_tourism_fee": None,
                            "dispatch_international_shipment_fee": 5.18350,   
                            "receipt_international_shipment_fee": 4.43410,                            
                            "last_updated": "2023-04-07T20:00:00"
                    },
                    "delivery": {
                        "exists": False,
                        "fee": None
                    }
                },
                {
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
                },
                {
                    "id": 3,
                    "name": "DayCâmbio",
                    "url": "daycambio",
                    "logo": "images/companies/daycambio/logo-daycambio.png",
                    "site": "https://daycambio.com.br/",
                    "principal_phone": {
                        "ddi": '55',
                        "ddd": '41',
                        "number": "99227122",
                        "full_number": "554199227122",                        
                        "is_whatsapp": False
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
            ]
        }
        
        return response
    
    def _mock_get_company_to_negotiation(self, filters):
        data = {
                "default_configuration": {                
                    "tourism_iof_percentage": 0.01100,
                    "international_shipment_iof_percentage": 0.03800,
                    "default_utc_datetime": 0
                },
                "filters": {
                    "modality": str(filters["modality"]).capitalize(),
                    "type": filters["type"], 
                    "coin": {
                        "url": filters["coin"],
                        "name": "Dólar americano"
                    }, 
                    "city": {
                        "url": filters["location"],
                        "name": "São Paulo",
                        "uf": "SP"
                    },
                    "companyid": filters["companyid"]
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
