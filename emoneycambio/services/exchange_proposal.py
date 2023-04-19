import logging
from sqlalchemy import exc
from emoneycambio.models.models import ExchangeProposalModel , db
from emoneycambio import utils
import json

LOGGER = logging.getLogger(__name__)
class ExchangeProposal:
    
    def __init__(self) -> None:
        pass
    
    def create_exchange_proposal(self,**data):
        """
        {
            'company_branch_id': None,
            'person_type': None,
            'transaction_type': None,
            'exchange_type': None,
            'reason': None,
            'total_value': None,
            'iof_fee': None,
            'vet': None,
            'coin_name': None,
            'document': None,
            'name': None,
            'responsible_name': None,
            'email': None,
            'phone': None,
            'phone_is_whatsapp': None,
            'delivery': None,
            'ip': None,
            'headers': None
        }
        """
        proposal = ExchangeProposalModel()        
        proposal.company_branch_id = data['company_branch_id']
        proposal.person_type = data['person_type']
        proposal.transaction_type = data['transaction_type']
        proposal.exchange_type = data['exchange_type']
        proposal.reason = data.get('reason')
        
        proposal.total_value = int(data['total_value']) / 100
        proposal.iof_fee = int(data['iof_fee']) / 100
        proposal.vet = int(data['vet']) / 100
        
        proposal.coin_name = data['coin_name']
        proposal.document = str(utils.only_numbers(data.get('document')))
        proposal.name = data['name']
        proposal.responsible_name = data.get('responsible_name')
        proposal.email = data['email']
        proposal.phone = utils.only_numbers(data['phone'])
        proposal.phone_is_whatsapp = data['phone_is_whatsapp']
        proposal.delivery = data['delivery']
        proposal.ip = data['ip']
        proposal.headers = json.dumps(dict(data['headers']))
        
        try:
            
            db.session.add(proposal)
            db.session.commit()
            return proposal.id

        except exc.IntegrityError as ex:
            LOGGER.error(str(ex))            
            return False    
        finally:
            db.session.flush()