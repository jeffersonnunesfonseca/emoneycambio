import logging
from sqlalchemy import exc
from emoneycambio.models.models import ExchangeCommercialCoinModel , db
from emoneycambio import utils

LOGGER = logging.getLogger(__name__)
class ExchangeCommercialCoin:
    
    def __init__(self) -> None:
        pass
    
    def get_updated_coins(self):
        
        coins = ExchangeCommercialCoinModel.query.all()
        return_coins = []
        for row in coins:
            result = (utils.transform_sqlalchemy_row_in_object(row))
            result['updated_at'] = result['updated_at'].isoformat() if result['updated_at'] else None
            result['created_at'] = result['created_at'].isoformat()
            return_coins.append(result)
            
        return return_coins
        
    def get_updated_coin_by_url(self, url):
        
        coin = ExchangeCommercialCoinModel.query.filter_by(url=url).first()
        return coin
        