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
    key = sa.Column(sa.String(length=150), nullable=False)    
    prefix = sa.Column(sa.String(length=10), nullable=False)    
    value = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))
    updated_at = sa.Column('updated_at', sa.DateTime())

class ExchangeCommercialCoinHistoryModel(db.Model):
     
    __tablename__ = 'exchange_commercial_coin_history'
    
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    exchange_commercial_coin_id = sa.Column(sa.Integer(), nullable=False)   
    value = sa.Column(sa.DECIMAL(asdecimal=False, precision=17, scale=5))
    created_at = sa.Column(sa.DateTime(), server_default=sa.text('now()'))

 