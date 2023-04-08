# companies
class Company:
    
    def __init__(self) -> None:
        pass
    
    def get_companies_by_coin_and_location(self, coin, company):
        pass
    
    def _mockCompanies(self):
        response = {
            "tourism_iof_percentage": 0.01100,
            "international_shipment_iof_percentage": 0.03800,
            "city": {
                "url": "sao-paulo-sp",
                "name": "São Paulo",
                "uf": "SP"
            },
            "companies": [
                {
                    "name": "Frente Corretora",
                    "url":"frente-corretora",
                    "logo": "logo-frente-corretora.png",
                    "site": "https://frentecorretora.com.br/",
                    "principal_phone": {
                        "ddi": "+55",
                        "ddd": "11",
                        "number": "42000850",
                        "full_number": "+551142000850",
                        "is_whatsapp": True
                    },
                    "coin": {
                            "name": "Dólar americano",
                            "prefix": "US$",
                            "buy_tourism_vet": 5.32720,
                            "sell_tourism_vet": None,
                            "dispatch_international_shipment_vet": 5.18350,   
                            "receipt_international_shipment_vet": 4.43410,
                    },
                    "delivery": {
                        "exists": False,
                        "fee": None
                    }
                },
                {
                    "name": "Get Money Câmbio",
                    "url":"get-money-cambio",
                    "logo": "logo-get-money-cambio.png",
                    "site": "https://www.getmoney.com.br/",
                    "principal_phone": {
                        "ddi": "+55",
                        "ddd": "11",
                        "number": "30181880",
                        "full_number": "+551130181880",
                        "is_whatsapp": True
                    },
                    "coin": {
                            "name": "Dólar americano",
                            "prefix": "US$",
                            "buy_tourism_vet": 5.28000,
                            "sell_tourism_vet": 4.99000,
                            "dispatch_international_shipment_vet": 5.16000,   
                            "receipt_international_shipment_vet": 4.94000,
                    },
                    "delivery": {
                        "exists": False,
                        "fee": None
                    }
                },
                {
                    "name": "DayCâmbio",
                    "url":"daycambio",
                    "logo": "logo-daycambio.png",
                    "site": "https://daycambio.com.br/",
                    "principal_phone": {
                        "ddi": None,
                        "ddd": None,
                        "number": "03001110500",
                        "full_number": "03001110500",                        
                        "is_whatsapp": False
                    },
                    "coin": {
                            "name": "Dólar americano",
                            "prefix": "US$",
                            "buy_tourism_vet": 5.28000,
                            "sell_tourism_vet": 4.99000,
                            "dispatch_international_shipment_vet": 5.16000,   
                            "receipt_international_shipment_vet": 4.94000,
                    },
                    "delivery": {
                        "exists": False,
                        "fee": None
                    }
                }
            ]
        }
    
    