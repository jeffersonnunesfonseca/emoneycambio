import logging
from sqlalchemy import exc
from emoneycambio.models.models import ExchangeCommercialCoinModel , db
from emoneycambio import utils
from datetime import datetime

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
    
    def create_exchange_commercial_coin_by_api(self, **data):
        """
            {
                "key": None,
                "name": None,
                "prefix": None,
                "value": None
            }
        """
        
        exchange_commercial_coin = ExchangeCommercialCoinModel()
        coin = ExchangeCommercialCoinModel.query.filter_by(key=data['key']).first()
        if coin:
            exchange_commercial_coin = coin
        else:                
            exchange_commercial_coin.name = data['name']
            exchange_commercial_coin.key = data['key']
            exchange_commercial_coin.prefix = data['prefix']
            
        exchange_commercial_coin.url = utils.string_to_url(data['name'])
        exchange_commercial_coin.symbol = exchange_commercial_coin.symbol or None
        exchange_commercial_coin.value = data['value']
        exchange_commercial_coin.updated_at = datetime.utcnow()
        try:                
            db.session.add(exchange_commercial_coin)
        
            db.session.commit()
            
        except exc.IntegrityError as ex:
            LOGGER.error(str(ex))   
            
            if "Duplicate" in str(ex):
                return
            
            raise ex
            
        finally:
            db.session.flush()