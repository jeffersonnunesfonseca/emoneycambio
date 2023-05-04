import logging
LOGGER = logging.getLogger(__name__)
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

from emoneycambio.config import SENDGRID_KEY

class SendGrid:
    def __init__(self) -> None:
        self._key = SENDGRID_KEY 
        self.from_ = "no-reply@emoneycambio.com.br"
        self.to_emails = None
        self.template_id = None
        self.params = None
        self.subject = None
        self.html_content = None
    
    def send_mail_dynamic_templates(self):

        try:
            message = Mail(
                from_email=(self.from_, "E-money Câmbio"),
                to_emails=self.to_emails
            )

            default_params = {
                "subject": self.subject 
            }
            
            if self.params:
                default_params.update(self.params)
                
            message.dynamic_template_data = default_params
            
            if self.template_id:
                message.template_id = self.template_id

            sg = sendgrid.SendGridAPIClient(api_key=self._key)
            
            response = sg.send(message)
            return response.status_code            
            # LOGGER.debug(response.status_code)
            # LOGGER.debug(response.headers)
        except Exception as ex:
            LOGGER.exception(str(ex))
            raise ex

    def send_mail_html(self):

        """Send Emails

        Send email to the mail ids

        :param emails: emails of the user
        :type emails: list
        :param notification_text: notification text
        :type notification_text: str
        :param request_link: link to the requet
        :type request_link: str
        :param subject: subject of the email
        :type subject: str

        :rtype: str
        """

        message = Mail(
            from_email=self.from_,
            to_emails=self.to_emails,
            subject=self.subject,
            html_content=self.html_content)
        try:
            sg = sendgrid.SendGridAPIClient(api_key=self._key)
            sg.send(message)
            return "Email Sent"
        
        except Exception as e:
            return e.message