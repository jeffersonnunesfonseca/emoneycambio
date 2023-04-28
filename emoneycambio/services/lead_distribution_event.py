import logging
from sqlalchemy import exc
from emoneycambio.models.models import LeadDistributionEventModel , db

LOGGER = logging.getLogger(__name__)
class LeadDistributionEvent:
    
    def __init__(self) -> None:
        pass
    
    def create_lead_distribution_event(self,**data):
        """
        {
            "company_branch_id": None,
            "origin_company_branch_id": None,
            "channel": None,enum('EMAIL','SMS','WHATSAPP','PARTNER_REGISTER')
            "product_type": None,enum('EXCHANGE_PROPOSAL','LOAN_PROPOSAL')
            "relationship_id": None

        }
        """
        event = LeadDistributionEventModel()  
        event.channel = data['channel']
        event.company_branch_id = data['company_branch_id']
        event.origin_company_branch_id = data['origin_company_branch_id']
        event.product_type = data['product_type']
        event.relationship_id = data.get('relationship_id')
        
        try:
            
            db.session.add(event)
            db.session.commit()
            return event.id

        except exc.IntegrityError as ex:
            LOGGER.error(str(ex))            
            return False    
        finally:
            db.session.flush()