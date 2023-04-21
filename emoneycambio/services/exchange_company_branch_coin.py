import logging
from sqlalchemy import exc
from emoneycambio.models.models import CompanyBranchExchangeCoinModel, CompanyBranchExchangeCoinHistoryModel , db
from emoneycambio.services.exchange_commercial_coin import ExchangeCommercialCoin
from emoneycambio.services.configuration import Configuration
from decimal import Decimal, ROUND_FLOOR
from emoneycambio import utils
from datetime import datetime
import json

LOGGER = logging.getLogger(__name__)

class CompanyBranchExchangeCoin:
    
    def __init__(self) -> None:
        self.exchange_commercial_coins = ExchangeCommercialCoin()
        self.configurations = Configuration()
    
    
    def create_company_branch_exchange_coin(self, **data):
        
        """
            {
                "company_branch_id": None,
                "name": None,
                "prefix": None,
                "buy_tourism_vet": None,
                "sell_tourism_vet": None,
                "dispatch_international_shipment_vet": None,
                "receipt_international_shipment_vet": None,
                "delivery": None,
                "delivery_value": None
            }
        """
        if not data.get('company_branch_id'):
            return False
        
        iof_buy_tourism_fee = self.configurations.get_global_iof_by_key('iof_buy_tourism_fee')
        iof_sell_tourism_fee = self.configurations.get_global_iof_by_key('iof_sell_tourism_fee')
        iof_international_shipment_fee = self.configurations.get_global_iof_by_key('iof_international_shipment_fee')
        
        url_coin = utils.string_to_url(data["name"])
        buy_tourism_exchange_fee = self._calc_exchange_fee_without_iof(data.get('buy_tourism_vet'), iof_buy_tourism_fee, url_coin)
        sell_tourism_exchange_fee = self._calc_exchange_fee_without_iof(data.get('sell_tourism_vet'), iof_sell_tourism_fee, url_coin)
        dispatch_international_shipment_exchange_fee = self._calc_exchange_fee_without_iof(data.get('dispatch_international_shipment_vet'), iof_international_shipment_fee, url_coin)
        receipt_international_shipment_exchange_fee = self._calc_exchange_fee_without_iof(data.get('receipt_international_shipment_vet'), iof_international_shipment_fee, url_coin)
        status = 'ENABLED'
        if not buy_tourism_exchange_fee and not sell_tourism_exchange_fee and not dispatch_international_shipment_exchange_fee and not receipt_international_shipment_exchange_fee:
            # status = 'DISABLED'
            LOGGER.info("Moeda nao localizada, skipando")
            return
        
        company_branch_exchange_coin = CompanyBranchExchangeCoinModel()
        current_company_branch_exchange_coin = CompanyBranchExchangeCoinModel \
            .query \
                .filter(CompanyBranchExchangeCoinModel.company_branch_id==data['company_branch_id'], 
                    CompanyBranchExchangeCoinModel.url_coin==url_coin) \
                        .first()
        
        if current_company_branch_exchange_coin:
            company_branch_exchange_coin = current_company_branch_exchange_coin
            company_branch_exchange_coin.updated_at = datetime.utcnow()
        
        
        
        company_branch_exchange_coin.company_branch_id = data['company_branch_id']
        company_branch_exchange_coin.url_coin = url_coin
        company_branch_exchange_coin.status = status
        company_branch_exchange_coin.prefix = data.get('prefix')
        company_branch_exchange_coin.name = str(data['name']).capitalize()
        company_branch_exchange_coin.buy_tourism_vet =  data.get('buy_tourism_vet') or company_branch_exchange_coin.buy_tourism_vet 
        company_branch_exchange_coin.sell_tourism_vet =  data.get('sell_tourism_vet') or company_branch_exchange_coin.sell_tourism_vet
        company_branch_exchange_coin.dispatch_international_shipment_vet =  data.get('dispatch_international_shipment_vet') or company_branch_exchange_coin.dispatch_international_shipment_vet
        company_branch_exchange_coin.receipt_international_shipment_vet =  data.get('receipt_international_shipment_vet') or company_branch_exchange_coin.receipt_international_shipment_vet
        company_branch_exchange_coin.buy_tourism_exchange_fee = buy_tourism_exchange_fee or company_branch_exchange_coin.buy_tourism_exchange_fee
        company_branch_exchange_coin.sell_tourism_exchange_fee = sell_tourism_exchange_fee or company_branch_exchange_coin.sell_tourism_exchange_fee
        company_branch_exchange_coin.dispatch_international_shipment_exchange_fee = dispatch_international_shipment_exchange_fee or company_branch_exchange_coin.dispatch_international_shipment_exchange_fee
        company_branch_exchange_coin.receipt_international_shipment_exchange_fee = receipt_international_shipment_exchange_fee or company_branch_exchange_coin.receipt_international_shipment_exchange_fee
        company_branch_exchange_coin.delivery = data.get('delivery') or 0
        company_branch_exchange_coin.delivery_value = data.get('delivery_value') or None
        
        
        

        

        try:
            
            db.session.add(company_branch_exchange_coin)
            
            db.session.commit()
            company_branch_exchange_coin_history = CompanyBranchExchangeCoinHistoryModel()            
            company_branch_exchange_coin_history.company_branch_exchange_coin_id = company_branch_exchange_coin.id
            company_branch_exchange_coin_history.buy_tourism_vet = company_branch_exchange_coin.buy_tourism_vet
            company_branch_exchange_coin_history.sell_tourism_vet = company_branch_exchange_coin.sell_tourism_vet
            company_branch_exchange_coin_history.dispatch_international_shipment_vet = company_branch_exchange_coin.dispatch_international_shipment_vet
            company_branch_exchange_coin_history.receipt_international_shipment_vet = company_branch_exchange_coin.receipt_international_shipment_vet
            company_branch_exchange_coin_history.buy_tourism_exchange_fee = company_branch_exchange_coin.buy_tourism_exchange_fee
            company_branch_exchange_coin_history.sell_tourism_exchange_fee = company_branch_exchange_coin.sell_tourism_exchange_fee
            company_branch_exchange_coin_history.dispatch_international_shipment_exchange_fee = company_branch_exchange_coin.dispatch_international_shipment_exchange_fee
            company_branch_exchange_coin_history.receipt_international_shipment_exchange_fee = company_branch_exchange_coin.receipt_international_shipment_exchange_fee
            company_branch_exchange_coin_history.iof_buy_tourism_fee = iof_buy_tourism_fee
            company_branch_exchange_coin_history.iof_sell_tourism_fee = iof_sell_tourism_fee
            company_branch_exchange_coin_history.iof_international_shipment_fee = iof_international_shipment_fee
            db.session.add(company_branch_exchange_coin_history)
            db.session.commit()
            return company_branch_exchange_coin.id

        except exc.IntegrityError as ex:
            LOGGER.error(str(ex))            
            return False    
        finally:
            db.session.flush()
    
    def _calc_exchange_fee_without_iof(self, vet: float, iof_fee, url: str):        
        
        if not vet or not iof_fee:
            return None
        vet = float(vet)
        iof_fee = float(iof_fee.value)
        
        commercial_coin = self.exchange_commercial_coins.get_updated_coin_by_url(url)
        if not commercial_coin:
            LOGGER.info(f"moeda nao configurada {url}")
            return None
        
        valor_sem_iof = vet - (vet * iof_fee) 
        taxa_corretora = (abs(valor_sem_iof-commercial_coin.value)/valor_sem_iof)
        taxa_corretora = Decimal(taxa_corretora).quantize(Decimal('.00000'), rounding=ROUND_FLOOR)
        return taxa_corretora