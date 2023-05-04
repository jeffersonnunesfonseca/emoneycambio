import logging
from sqlalchemy import exc
from emoneycambio.models.models import ContactUsModel , db
from emoneycambio import utils
from emoneycambio.services.mail import SendGrid

LOGGER = logging.getLogger(__name__)
class ContactUs:
    
    def __init__(self) -> None:
        pass
    
    def create_contact_us(self, **data):
        """
        {
            'reason_contact': 'sugestao',
            'name': 'jefferson nunes',
            'phone': '(41) 99756-0263',
            'is_whatsapp': 1,
            'email': 'jeffersonnunesfonsec@gmail.com',
            'description_contact': 'sasasa'
        }
        """
        contact = ContactUsModel()  
        contact.reason = data['reason_contact']
        contact.name = data['name']
        contact.phone = utils.only_numbers(data['phone'])
        contact.phone_is_whatsapp = data.get('is_whatsapp')
        contact.email = data['email']
        contact.description = data['description_contact']
        
        try:
            
            db.session.add(contact)
            db.session.commit()
            # for email in to_emails:
            try:
                action = SendGrid()                    
                # action.template_id = config.SENDGRID_TEMPLATE_PROPOSAL_CLIENT_ID
                # action.params = params_to_client
                action.subject = f'#{contact.id} Nova mensagem no formulário de contato'
                action.to_emails = "emoneycambio@gmail.com"
                action.html_content = f"""
                    <ul>
                        <li>Motivo: {contact.reason}</li>
                        <li>Nome: {contact.name}</li>
                        <li>Telefone: {contact.phone}</li>
                        <li>é whats?: {contact.phone_is_whatsapp}</li>
                        <li>Email: {contact.email}</li>
                        <li>Descrição: {contact.description}</li>
                    </ul>
                """
                result_email_client = action.send_mail_html()
                LOGGER.info(f"email enviado com sucesso para a equipe")
            except Exception as ex:
                LOGGER.error(f"Problema ao enviar email para equipe{str(ex)}")
                return 'error'
            return contact.id

        except exc.IntegrityError as ex:
            LOGGER.error(str(ex))            
            return False    
        finally:
            db.session.flush()