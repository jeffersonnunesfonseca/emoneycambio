import logging
from sqlalchemy import exc
from emoneycambio.models.models import CompanyBranchModel , db
from decimal import Decimal, ROUND_FLOOR
from emoneycambio import utils
from sqlalchemy.sql import text
from datetime import datetime
import json

LOGGER = logging.getLogger(__name__)

class CompanyBranch:
    
    def __init__(self) -> None:
        self.db_session = db.session
    
    def get_company_branch_by_company_url_and_url_location(self, company_url, localtion_url):
        sql = f"""
            select 
                c.id as original_company_id, 
                c.fantasy_name as name,
                cb.site,
                cb.id as company_branch_id,
                cb.principal
            from company c
            left join company_branch cb on c.id = cb.company_id and cb.url_location = '{localtion_url}' and cb.status = 'ENABLED'
            where 
            c.status = 'ENABLED'                   
            and c.url = '{company_url}'
            
        """
        return self.db_session.execute(text(sql)).fetchone()
    
    def create_company_branch(self, **data):        
        """
            {
                "company_id": None,
                "principal": None,
                "name": None,
                "site": None,
                "full_address": None,
                "complement": None,
                "uf": None,
                "city": None,
                "cep": None,
                "lat": None,
                "lng": None
            }
        """
        if not data.get("company_id"):
            return False
        
        url_location = f"{utils.string_to_url(data['city'])}-{utils.string_to_url(data['uf'])}"
        company_branch = CompanyBranchModel()
        current_company_branch = CompanyBranchModel.query \
                .filter(CompanyBranchModel.url_location==url_location, 
                        CompanyBranchModel.company_id==data["company_id"]).first()

        if current_company_branch:
            company_branch = current_company_branch
            company_branch.updated_at = datetime.utcnow()
        
        company_branch.company_id = data["company_id"]
        company_branch.principal = data.get("principal") or 0
        company_branch.name = str(data['name']).capitalize()
        company_branch.status = 'ENABLED'
        company_branch.site = data.get("site") or None
        company_branch.full_address = data.get("full_address") or None
        company_branch.complement = data.get("complement") or None
        company_branch.uf = str(data['uf']).upper()
        company_branch.city = str(data['city']).capitalize()
        company_branch.url_location = url_location
        company_branch.cep = utils.only_numbers(data.get("cep")) or None
        
        latitude = data.get('lat') or None
        longitude = data.get('lng') or None     
        company_branch.coordinates = None
        if latitude and longitude:
            company_branch.coordinates = f"{latitude}, {longitude}"
        
        try:
            
            db.session.add(company_branch)
            db.session.commit()
            return company_branch.id

        except exc.IntegrityError as ex:
            LOGGER.error(str(ex))            
            return False    
        finally:
            db.session.flush()
    