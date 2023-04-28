import enum
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from emoneycambio.resources.database import db

@enum.unique
class PersonType(enum.Enum):    
    PF = 'PF'
    PJ = 'PJ'
    
@enum.unique
class TransactionType(enum.Enum):    
    BUY = 'BUY'
    SELL = 'SELL'
    SEND = 'SEND'
    RECEIVE = 'RECEIVE'

class ExchangeType(enum.Enum):    
    TOURISM = 'TOURISM'
    INTERNATIONAL_SHIPMENT = 'INTERNATIONAL_SHIPMENT'

class Status(enum.Enum):
    
    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'
class ContactType(enum.Enum):
    
    PHONE = 'PHONE'
    CELLPHONE = 'CELLPHONE'
    WHATSAPP = 'WHATSAPP'
    EMAIL = 'EMAIL'

class ChannelType(enum.Enum):
    
    PARTNER_REGISTER = 'PARTNER_REGISTER'
    WHATSAPP = 'WHATSAPP'
    SMS = 'SMS'
    EMAIL = 'EMAIL'

class ProductType(enum.Enum):
    
    EXCHANGE_PROPOSAL = 'EXCHANGE_PROPOSAL'
    LOAN_PROPOSAl = 'LOAN_PROPOSAl'

class ExchangeProposalModel(db.Model):
    __tablename__ = 'exchange_proposal'
    
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    company_branch_id = sa.Column(sa.Integer(), nullable=False)
    person_type = sa.Column(sa.Enum(*[e.value for e in PersonType]), nullable=False)    
    transaction_type = sa.Column(sa.Enum(*[e.value for e in TransactionType]), nullable=False)    
    exchange_type = sa.Column(sa.Enum(*[e.value for e in ExchangeType]), nullable=False)    
    reason = sa.Column(sa.String(length=100), nullable=True)    
    total_value = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    iof_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    coin_name = sa.Column(sa.String(length=150), nullable=False)    
    document = sa.Column(sa.String(length=14), nullable=True)    
    name = sa.Column(sa.String(length=150), nullable=False) 
    responsible_name = sa.Column(sa.String(length=150), nullable=True) 
    email = sa.Column(sa.String(length=150), nullable=False) 
    phone = sa.Column(sa.String(length=13), nullable=False) 
    phone_is_whatsapp = sa.Column(sa.SmallInteger(), nullable=False) 
    delivery = sa.Column(sa.SmallInteger(), nullable=False) 
    ip = sa.Column(sa.String(length=200), nullable=False)  
    user_agent = sa.Column(sa.Text(), nullable=False)  
    headers = sa.Column(sa.Text(), nullable=False)  
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))
    
class ExchangeCommercialCoinModel(db.Model):
    
    __tablename__ = 'exchange_commercial_coin'
    
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(length=150), nullable=False)   
    url = sa.Column(sa.String(length=200), nullable=False)    
    key = sa.Column(sa.String(length=150), nullable=False)    
    prefix = sa.Column(sa.String(length=10), nullable=False)
    symbol = sa.Column(sa.String(length=10), nullable=False)    
    value = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))
    updated_at = sa.Column('updated_at', sa.DateTime())

class CompanyBranchExchangeCoinModel(db.Model):
    
    __tablename__ = 'company_branch_exchange_coin'
   
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    company_branch_id = sa.Column(sa.Integer(), nullable=False)
    name = sa.Column(sa.String(length=150), nullable=False)   
    url_coin = sa.Column(sa.String(length=150), nullable=False)   
    prefix = sa.Column(sa.String(length=10), nullable=False)    
    status = sa.Column(sa.Enum(*[e.value for e in Status]), nullable=False)    
    buy_tourism_vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    sell_tourism_vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    dispatch_international_shipment_vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    receipt_international_shipment_vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    buy_tourism_exchange_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    sell_tourism_exchange_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    dispatch_international_shipment_exchange_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    receipt_international_shipment_exchange_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    delivery = sa.Column(sa.SmallInteger(), nullable=False) 
    delivery_value = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))
    updated_at = sa.Column('updated_at', sa.DateTime())
    
class CompanyBranchExchangeCoinHistoryModel(db.Model):
    
    __tablename__ = 'company_branch_exchange_coin_history'
   
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    company_branch_exchange_coin_id = sa.Column(sa.Integer(), nullable=False)
    buy_tourism_vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    sell_tourism_vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    dispatch_international_shipment_vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    receipt_international_shipment_vet = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    buy_tourism_exchange_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    sell_tourism_exchange_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    dispatch_international_shipment_exchange_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    receipt_international_shipment_exchange_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    iof_buy_tourism_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    iof_sell_tourism_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    iof_international_shipment_fee = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))

class ConfigurationModel(db.Model):
    
    __tablename__ = 'configuration'
   
    key = sa.Column(sa.String(255), primary_key=True)
    value = sa.Column(sa.String(length=255), nullable=False)   
    description = sa.Column(sa.String(length=255))   
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))
    updated_at = sa.Column('updated_at', sa.DateTime())

class CompanyBranchModel(db.Model):
    
    __tablename__ = 'company_branch'

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    company_id = sa.Column(sa.Integer(), nullable=False)
    principal = sa.Column(sa.SmallInteger(), nullable=False) 
    name = sa.Column(sa.String(length=150), nullable=False)   
    site = sa.Column(sa.String(length=200))   
    full_address = sa.Column(sa.String(length=350))      
    complement = sa.Column(sa.String(length=150))  
    uf = sa.Column(sa.String(length=2), nullable=False)  
    city = sa.Column(sa.String(length=150), nullable=False)  
    url_location = sa.Column(sa.String(length=150), nullable=False)  
    cep = sa.Column(sa.String(length=8))  
    coordinates = sa.Column(sa.String(length=350)) 
    status = sa.Column(sa.Enum(*[e.value for e in Status]), nullable=False)    
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))
    updated_at = sa.Column('updated_at', sa.DateTime())

class CompanyBranchContactModel(db.Model):
    
    __tablename__ = 'company_branch_contact'

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    company_branch_id = sa.Column(sa.Integer(), nullable=False)
    type = sa.Column(sa.Enum(*[e.value for e in ContactType]), nullable=False)    
    principal = sa.Column(sa.SmallInteger(), nullable=False)     
    value = sa.Column(sa.String(length=200), nullable=False) 
    status = sa.Column(sa.Enum(*[e.value for e in Status]), nullable=False)    
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))
    updated_at = sa.Column('updated_at', sa.DateTime())

class LeadDistributionEventModel(db.Model):
    
    __tablename__ = 'lead_distribution_event'

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    company_branch_id = sa.Column(sa.Integer(), nullable=False)
    origin_company_branch_id = sa.Column(sa.Integer(), nullable=False)
    channel = sa.Column(sa.Enum(*[e.value for e in ChannelType]), nullable=False)    
    product_type = sa.Column(sa.Enum(*[e.value for e in ProductType]), nullable=False)    
    relationship_id = sa.Column(sa.Integer())
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))
    updated_at = sa.Column('updated_at', sa.DateTime())