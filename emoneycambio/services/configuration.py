from emoneycambio.models.models import ConfigurationModel , db
from emoneycambio import utils
class Configuration:
    
    def __init__(self) -> None:
        pass
    
    def get_global_iof_by_key(self, key):
        fee = ConfigurationModel.query.filter_by(key=key).first()
        
        return fee
    
    def get_all_leads_distribution_to(self):
        """ Caso exista, retorna o adapter de qual company deve ir todos os leads, caso nao exista deve ser enviado para a company originaria """
        config = ConfigurationModel.query.filter_by(key='all_lead_distribution_to').first()
        if config:
            return config.value
        return None