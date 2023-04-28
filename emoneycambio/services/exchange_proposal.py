import logging
from sqlalchemy import exc
from emoneycambio.models.models import ExchangeProposalModel , db
from emoneycambio.services.mail import SendGrid
from emoneycambio.services.configuration import Configuration
from emoneycambio.services.company_branch_contact import CompanyBranchContact
from emoneycambio.services.lead_distribution_event import LeadDistributionEvent
from emoneycambio import utils, config
import json

LOGGER = logging.getLogger(__name__)
class ExchangeProposal:
    
    def __init__(self) -> None:
        pass
    
    def create_exchange_proposal(self,**data):
        """
        {
            'company_branch_id': None,
            'company_name': None,
            'company_url': None,
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
        proposal.document = str(utils.only_numbers(data.get('document'))).zfill(11)
        proposal.name = data['name']
        proposal.responsible_name = data.get('responsible_name')
        proposal.email = data['email']
        proposal.phone = utils.only_numbers(data['phone'])
        proposal.phone_is_whatsapp = data['phone_is_whatsapp']
        proposal.delivery = data['delivery']
        proposal.user_agent = data['user_agent']        
        proposal.ip = data['ip']
        proposal.headers = json.dumps(dict(data['headers']))
        
        try:
            
            db.session.add(proposal)
            db.session.commit()

            # envia email para cliente
            params_to_client = {
                "client_name": proposal.responsible_name or proposal.name,
                "company_name": data.get('company_name')
            }

            # for email in to_emails:
            try:
                action_to_client = SendGrid()                    
                action_to_client.template_id = config.SENDGRID_TEMPLATE_PROPOSAL_CLIENT_ID
                action_to_client.params = params_to_client
                action_to_client.subject = f'Emoney Câmbio | Proposta enviada'
                action_to_client.to_emails = proposal.email
                result_email_client = action_to_client.send_mail_dynamic_templates()
                LOGGER.info(f"email enviado com sucesso para cliente")
            except Exception as ex:
                LOGGER.error(f"Problema ao enviar email para cliente{str(ex)}")
                return 'error'

            if result_email_client not in [200, 201, 202]:
                LOGGER.info(f"problema ao enviar email para o cliente, {result_email_client}")
                return 'error'
            
            # verifica se deve enviar lead para alguem especifico
            company_url = data['company_url']
            config_db = Configuration()        
            company_url_configuration = config_db.get_all_leads_distribution_to()
            if company_url_configuration:
                company_url = company_url_configuration
            
            LOGGER.info(f"company url {company_url}")
            
            # pega contato
            contact = CompanyBranchContact()        
            contact_result = contact.get_principal_email_contact_by_company_url(company_url)
            LOGGER.info(f"company_email_contact {contact_result['contact']}")
            LOGGER.info(f"company_branch_id {contact_result['company_branch_id']}")
            if not contact_result['contact']:
                LOGGER.error(f"company não possui email, envia para emoneycambio@gmail.com")
                contact_result['contact'] = "emoneycambio@gmail.com"
            
            # cadastra evento
            data_event = {
                "company_branch_id": contact_result['company_branch_id'],
                "origin_company_branch_id": proposal.company_branch_id,
                "channel": "EMAIL",
                "product_type": "EXCHANGE_PROPOSAL",
                "relationship_id": proposal.id
            }
        
            lead = LeadDistributionEvent()        
            lead.create_lead_distribution_event(**data_event)
            
            # envia email para company
            try:

                # 'RECEIVE' if transaction == 'receber' else 'SEND',
                # 'BUY' if modality == 'comprar' else 'SELL',
                transaction_type_translate = None
                if proposal.transaction_type == 'RECEIVE':
                    transaction_type_translate='RECEBER'
                elif proposal.transaction_type == 'SEND':
                    transaction_type_translate='ENVIAR'
                elif proposal.transaction_type == 'BUY':
                    transaction_type_translate='COMPRAR'
                elif proposal.transaction_type == 'SELL':
                    transaction_type_translate='VENDER'

                params_to_company = {
                    "client_name": proposal.name or proposal.responsible_name,
                    "responsible_name":proposal.responsible_name or proposal.name,
                    "company_name": contact_result['company_branch_name'],
                    "client_type": proposal.person_type,
                    "transaction_type": transaction_type_translate,
                    "coin": proposal.coin_name,
                    "document": proposal.document,
                    "email": proposal.email,
                    "phone": proposal.phone,
                    "is_whatsapp": "Sim" if proposal.phone_is_whatsapp == 1 else "Não",
                    "is_delivery": "Sim" if proposal.delivery == 1 else "Não",
                    "exchange_type": "Turismo" if proposal.exchange_type == 'TOURISM' else 'Remessa Internacional',
                    "total_value":f"R$ {proposal.total_value}",
                    "vet": f"R$ {proposal.vet}",
                    "fantasy_name": data.get('company_name'),
                    "ip": proposal.ip,
                    "reason": utils.de_para_reasons(proposal.reason),
                    "user_agent": proposal.user_agent
                }
                action_to_company = SendGrid()                    
                action_to_company.template_id = config.SENDGRID_TEMPLATE_PROPOSAL_COMPANY_ID
                action_to_company.params = params_to_company
                action_to_company.subject = f'Emoney Câmbio | Proposta recebida de um cliente'
                action_to_company.to_emails = contact_result['contact']
                action_to_company.send_mail_dynamic_templates()
                LOGGER.info(f"email enviado com sucesso para cliente")
            except Exception as ex:
                LOGGER.error(f"Problema ao enviar email para a company{str(ex)}")

            return proposal.id

        except exc.IntegrityError as ex:
            LOGGER.error(str(ex))            
            return False    
        finally:
            db.session.flush()

    