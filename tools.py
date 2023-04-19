import fire
import logging
import requests
from datetime import datetime
from sqlalchemy import exc

from emoneycambio.app import app


LOGGER = logging.getLogger(__name__)
def update_exchange_commercial_coin():
    from emoneycambio.resources.database import db
    from emoneycambio.models.models import ExchangeCommercialCoinModel, ExchangeCommercialCoinHistoryModel
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
                exchange_commercial_coin.prefix = value['coidein']
                
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
            
if __name__ == "__main__":
    fire.Fire()