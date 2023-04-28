import logging
from sqlalchemy import exc
from emoneycambio.models.models import CompanyBranchContactModel , db
from decimal import Decimal, ROUND_FLOOR
from emoneycambio import utils
from sqlalchemy.sql import text
from datetime import datetime
import json

LOGGER = logging.getLogger(__name__)

class CompanyBranchContact:
    
    def __init__(self) -> None:
        self.db_session = db.session

    def create_company_branch_contact(self, **data):        
        """
            {
                "company_branch_id": None,
                "type": None,
                "principal": None,
                "value": None,
            }
        """
        if not data.get("company_branch_id"):
            return False
        
        company_branch_contact = CompanyBranchContactModel()
        current_company_branch_contact = CompanyBranchContactModel.query \
            .filter(CompanyBranchContactModel.company_branch_id==data.get("company_branch_id")).first()

        if current_company_branch_contact:
            company_branch_contact = current_company_branch_contact
            company_branch_contact.updated_at = datetime.utcnow()
        
        company_branch_contact.company_branch_id = data["company_branch_id"]
        company_branch_contact.type = str(data["type"]).upper()
        company_branch_contact.principal = data.get('principal') or 0
        
        value = data["value"]
        if  str(data["type"]).upper() != "EMAIL":
            value = utils.only_numbers(value)
        
        company_branch_contact.value = value
        try:
            
            db.session.add(company_branch_contact)
            db.session.commit()
            return company_branch_contact.id

        except exc.IntegrityError as ex:
            LOGGER.error(str(ex))            
            return False    
        finally:
            db.session.flush()
    
    def get_contact_by_company_branch_id(self, company_branch_id):
        sql = f"select * from company_branch_contact where company_branch_id = {company_branch_id} and status = 'ENABLED' and principal=1"
        return self.db_session.execute(text(sql)).fetchone()
    
    def get_principal_email_contact_by_company_url(self, company_url):
        """ retorna principal contato de uma company, caso nao tenha um company_branch principal retorna a primeira que tiver contato"""
        
        sql = f"""
        select cb.principal as company_branch_principal,cb.name as company_branch_name, cbc.* from company c
        inner join company_branch cb on cb.company_id = c.id
        inner join company_branch_contact cbc on cbc.company_branch_id = cb.id
        where 1=1
            and c.status = 'ENABLED'
            and cb.status = 'ENABLED'
            and cbc.status = 'ENABLED'
            and cbc.type = 'EMAIL'
            and c.url = '{company_url}'
            
            order by company_branch_id desc;
        """
        results = self.db_session.execute(text(sql)).fetchall()
        if not results:
            LOGGER.error(f"company nao possui contato {company_url}")
            return
        
        company_branch_id = results[0].company_branch_id
        for result in results:
            if result.company_branch_principal == 1:
                company_branch_id = result.company_branch_id
                break
        
        contacts = []
        for result in results:
            if result.company_branch_id == company_branch_id:
                contacts.append(result)
        
        contact = contacts[0].value
        company_branch_name = contacts[0].company_branch_name
        for c in contacts:
            if c.principal == 1:
                contact = c.value
                break
        
        data_return = {
            "contact": contact,
            "company_branch_id": company_branch_id,
            "company_branch_name": company_branch_name
        }
        return data_return

        
    