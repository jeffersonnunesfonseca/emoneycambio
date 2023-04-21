from emoneycambio.app import app
from emoneycambio.resources.database import db
from sqlalchemy.sql import text

class SeedDB:
    def __init__(self) -> None:
        self.db_session = db.session
        self.app = app
        
    def make_frente_corretora(self):
        
        # sao paulo
        sql_company = "INSERT INTO `company` (`cnpj`, `name`, `fantasy_name`, `url`, `logo_name`) VALUES ('71677850000177', \
            'A Frente Corretora de Câmbio LTDA', 'Frente Corretora', 'frente-corretora', 'logo-frente-corretora.png')"
        result_company = self.db_session.execute(text(sql_company))
                
    def make_get_money_cambio(self):
        
        sql_company = "INSERT INTO `company` (`cnpj`, `name`, `fantasy_name`, `url`, `logo_name`) VALUES ('10853017000145', \
            'GET MONEY CORRETORA DE CAMBIO S.A', 'Get Money Câmbio', 'get-money-cambio', 'logo-get-money-cambio.png')"
        result_company = self.db_session.execute(text(sql_company))
        
    def make_daycambio(self):
        sql_company = "INSERT INTO `company` (`cnpj`, `name`, `fantasy_name`, `url`, `logo_name`) VALUES ('02759908000109', \
            'IFP PROMOTORA DE SERVIÇOS DE CONSULTORIA DE CADASTRO LTDA', 'Daycambio', 'daycambio', 'logo-daycambio.png')"
        result_company = self.db_session.execute(text(sql_company))
                        
    def make_configuration(self):
        sqls = [
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('iof_buy_tourism_fee', '0.011', 'Taxa IOF global de compra turismo')",
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('iof_sell_tourism_fee', '0.0038', 'Taxa IOF global de venda turismo')",
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('iof_international_shipment_fee', '0.0038', 'Taxa IOF global remessa internacional')",
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('all_lead_distribution_to', 'daycambio', 'Todos os leads serão enviado apenas para a company que tiver cadastrada')",
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('allowed_companies_international_shipment', 'frente-corretora|', 'Empresa que estará configurada para remessa internacional')"            
        ] 
        for sql in sqls:
            self.db_session.execute(text(sql))

    def make_commercial_coins(self):
        sqls = [
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `symbol`, `value`, `key`, `url`) VALUES ('Dólar Americano', 'USD', 'US$', '4.97', 'USDBRL','dolar-americano')",
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `symbol`, `value`, `key`, `url`) VALUES ('Dólar Canadense', 'CAD', 'C$', '3.71', 'CADBRL','dolar-canadense')",
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `symbol`,`value`, `key`, `url`) VALUES ('Bitcoin', 'BTC', 'B$', '150.264,20', 'BTCBRL','bitcoin')",
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `symbol`, `value`, `key`, `url`) VALUES ('Euro', 'EUR', '€', '5.45', 'EURBRL', 'euro')",
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `symbol`, `value`, `key`, `url`) VALUES ('Libra esterlina', 'GBP', '£', '6.17', 'GBPBRL','libra-esterlina')",

        ]
        for sql in sqls:
            self.db_session.execute(text(sql))
    
    def execute(self):
        with self.app.app_context() as apps:
            self.make_configuration()
            self.make_commercial_coins()
            self.make_frente_corretora()            
            self.make_get_money_cambio()
            self.make_daycambio()
            self.db_session.commit()
    