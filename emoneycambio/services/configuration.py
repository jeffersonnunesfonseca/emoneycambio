from emoneycambio.models.models import ConfigurationModel , db
from emoneycambio import utils
class Configuration:
    
    def __init__(self) -> None:
        pass
    
    def get_global_iof_by_key(self, key):
        # fees = ConfigurationModel.query.filter(ConfigurationModel.key.in_(["iof_buy_tourism_fee", "iof_sell_tourism_fee", 
        #                                                              "iof_international_shipment_fee"])) \
        #                                                                  .first()

        fee = ConfigurationModel.query.filter_by(key=key).first()
        
        return fee