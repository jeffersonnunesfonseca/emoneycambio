from emoneycambio.app import create_app
from emoneycambio.resources.database import db
from sqlalchemy.sql import text

class SeedDB:
    def __init__(self) -> None:
        self.db_session = db.session
        self.app = app = create_app()
        
    def make_frente_corretora(self):
        sql_company = "INSERT INTO `company` (`cnpj`, `name`, `fantasy_name`, `url`, `logo_name`) VALUES ('71677850000177', \
            'A Frente Corretora de Câmbio LTDA', 'Frente Corretora', 'frente-corretora', 'logo-frente-corretora.png')"
        result_company = self.db_session.execute(text(sql_company))
        
        sql_company_branch = f"INSERT INTO `emoneycambio`.`company_branch` (`company_id`, `principal`, `name`, `site`, \
            `full_address`, `complement`, `uf`, `city`,`url_location`,`cep`, `coordinates`) \
                VALUES ('{result_company.lastrowid}', '1', 'Frente Corretora', 'https://frentecorretora.com.br/', 'R. Fidêncio Ramos, 100 – Vila Olímpia', \
                    '7º andar', 'SP', 'São Paulo', 'sao-paulo-sp','04551010' \
                        ,ST_GeomFromText('POINT(0 0)'))"
        result_company_branch = self.db_session.execute(text(sql_company_branch))
        
        sql_company_branch_contact = f"INSERT INTO `emoneycambio`.`company_branch_contact` (`company_branch_id`, `type`, \
            `principal`, `value`) VALUES ('{result_company_branch.lastrowid}', 'PHONE', '1', '551142000850')"
            
        result_company_branch_contact = self.db_session.execute(text(sql_company_branch_contact))

        sql_company_branch_exchange_coin = f"INSERT INTO `emoneycambio`.`company_branch_exchange_coin` \
            (`company_branch_id`, `name`, `url_coin`, `prefix`, `buy_tourism_vet`, `sell_tourism_vet`, \
                `dispatch_international_shipment_vet`, `receipt_international_shipment_vet`, `buy_tourism_exchange_fee`, \
                    `sell_tourism_exchange_fee`, `dispatch_international_shipment_exchange_fee`, \
                        `receipt_international_shipment_exchange_fee`) VALUES ('{result_company_branch.lastrowid}', 'Dólar Americano', 'dolar-americano', \
                            'US$', '5.2409', '', '5.0934', '4.357', '2', NULL, '2', '2')"
        
        result_company_branch_exchange_coin = self.db_session.execute(text(sql_company_branch_exchange_coin))
        

        sql_company_branch_exchange_coin_history = f"INSERT INTO `emoneycambio`.`company_branch_exchange_coin_history` \
            (`company_branch_exchange_coin_id`, `buy_tourism_vet`, `dispatch_international_shipment_vet`, \
                `receipt_international_shipment_vet`, `buy_tourism_exchange_fee`, \
                    `dispatch_international_shipment_exchange_fee`, `receipt_international_shipment_exchange_fee`, \
                        `iof_tourism_fee`, `iof_international_shipment_fee`) \
                            VALUES ('{result_company_branch_exchange_coin.lastrowid}', '1', '1', '1', '1', '1', '1', '1', '1');"

        result_company_branch_exchange_coin_history = self.db_session.execute(text(sql_company_branch_exchange_coin_history))
        
    def make_get_money_cambio(self):
        
        sql_company = "INSERT INTO `company` (`cnpj`, `name`, `fantasy_name`, `url`, `logo_name`) VALUES ('10853017000145', \
            'GET MONEY CORRETORA DE CAMBIO S.A', 'Get Money Câmbio', 'get-money-cambio', 'logo-get-money-cambio.png')"
        result_company = self.db_session.execute(text(sql_company))
        
        sql_company_branch = f"INSERT INTO `emoneycambio`.`company_branch` (`company_id`, `principal`, `name`, `site`, \
            `full_address`, `complement`, `uf`, `city`,`url_location`,`cep`, `coordinates`) \
                VALUES ('{result_company.lastrowid}', '1', 'Get Money Câmbio', 'https://www.getmoney.com.br/', 'Av. Ibirapuera, 3103 - Piso Moema', \
                    'Piso: Moema - Loja 59 - Fica ao lado do Itaú (nossa loja fica no ultimo piso de cima)', 'SP', 'São Paulo', 'sao-paulo-sp','00000000' \
                        ,ST_GeomFromText('POINT(0 0)'))"
        result_company_branch = self.db_session.execute(text(sql_company_branch))
        
        sql_company_branch_contact = f"INSERT INTO `emoneycambio`.`company_branch_contact` (`company_branch_id`, `type`, \
            `principal`, `value`) VALUES ('{result_company_branch.lastrowid}', 'WHATSAPP', '1', '5511973629335')"
            
        result_company_branch_contact = self.db_session.execute(text(sql_company_branch_contact))

        sql_company_branch_exchange_coin = f"INSERT INTO `emoneycambio`.`company_branch_exchange_coin` \
            (`company_branch_id`, `name`, `url_coin`, `prefix`, `buy_tourism_vet`, `sell_tourism_vet`, \
                `dispatch_international_shipment_vet`, `receipt_international_shipment_vet`, `buy_tourism_exchange_fee`, \
                    `sell_tourism_exchange_fee`, `dispatch_international_shipment_exchange_fee`, \
                        `receipt_international_shipment_exchange_fee`) VALUES ('{result_company_branch.lastrowid}', 'Dólar Americano', 'dolar-americano', \
                            'US$', '5.17', '4.92', '5.05', '4.87', '2', 2, '2', '2')"
        
        result_company_branch_exchange_coin = self.db_session.execute(text(sql_company_branch_exchange_coin))
        

        sql_company_branch_exchange_coin_history = f"INSERT INTO `emoneycambio`.`company_branch_exchange_coin_history` \
            (`company_branch_exchange_coin_id`, `buy_tourism_vet`, `dispatch_international_shipment_vet`, \
                `receipt_international_shipment_vet`, `buy_tourism_exchange_fee`, \
                    `dispatch_international_shipment_exchange_fee`, `receipt_international_shipment_exchange_fee`, \
                        `iof_tourism_fee`, `iof_international_shipment_fee`) \
                            VALUES ('{result_company_branch_exchange_coin.lastrowid}', '1', '1', '1', '1', '1', '1', '1', '1');"

        result_company_branch_exchange_coin_history = self.db_session.execute(text(sql_company_branch_exchange_coin_history))

    def make_daycambio(self):
        sql_company = "INSERT INTO `company` (`cnpj`, `name`, `fantasy_name`, `url`, `logo_name`) VALUES ('02759908000109', \
            'IFP PROMOTORA DE SERVIÇOS DE CONSULTORIA DE CADASTRO LTDA', 'Daycambio', 'daycambio', 'logo-daycambio.png')"
        result_company = self.db_session.execute(text(sql_company))
        
        sql_company_branch = f"INSERT INTO `emoneycambio`.`company_branch` (`company_id`, `principal`, `name`, `site`, \
            `full_address`, `complement`, `uf`, `city`,`url_location`,`cep`, `coordinates`) \
                VALUES ('{result_company.lastrowid}', '1', 'Daycambio', 'https://daycambio.com.br/', 'Av. José Pinheiro Borges', \
                    'Shopping Itaquera', 'SP', 'São Paulo', 'sao-paulo-sp','08220900' \
                        ,ST_GeomFromText('POINT(0 0)'))"
        result_company_branch = self.db_session.execute(text(sql_company_branch))
        
        sql_company_branch_contact = f"INSERT INTO `emoneycambio`.`company_branch_contact` (`company_branch_id`, `type`, \
            `principal`, `value`) VALUES ('{result_company_branch.lastrowid}', 'PHONE', '1', '551142000850')"
            
        result_company_branch_contact = self.db_session.execute(text(sql_company_branch_contact))

        sql_company_branch_exchange_coin = f"INSERT INTO `emoneycambio`.`company_branch_exchange_coin` \
            (`company_branch_id`, `name`, `url_coin`, `prefix`, `buy_tourism_vet`, `sell_tourism_vet`, \
                `dispatch_international_shipment_vet`, `receipt_international_shipment_vet`, `buy_tourism_exchange_fee`, \
                    `sell_tourism_exchange_fee`, `dispatch_international_shipment_exchange_fee`, \
                        `receipt_international_shipment_exchange_fee`) VALUES ('{result_company_branch.lastrowid}', 'Dólar Americano', 'dolar-americano', \
                            'US$', '5.2409', '', '5.0934', '4.357', '2', NULL, '2', '2')"
        
        result_company_branch_exchange_coin = self.db_session.execute(text(sql_company_branch_exchange_coin))
        

        sql_company_branch_exchange_coin_history = f"INSERT INTO `emoneycambio`.`company_branch_exchange_coin_history` \
            (`company_branch_exchange_coin_id`, `buy_tourism_vet`, `dispatch_international_shipment_vet`, \
                `receipt_international_shipment_vet`, `buy_tourism_exchange_fee`, \
                    `dispatch_international_shipment_exchange_fee`, `receipt_international_shipment_exchange_fee`, \
                        `iof_tourism_fee`, `iof_international_shipment_fee`) \
                            VALUES ('{result_company_branch_exchange_coin.lastrowid}', '1', '1', '1', '1', '1', '1', '1', '1');"

        result_company_branch_exchange_coin_history = self.db_session.execute(text(sql_company_branch_exchange_coin_history))
        
    def make_configuration(self):
        sqls = [
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('iof_tourism_fee', '0.011', 'Taxa IOF global turismo')",
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('iof_international_shipment_fee', '0.0038', 'Taxa IOF global remessa internacional')",
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('all_lead_distribution_to', 'daycambio', 'Todos os leads serão enviado apenas para a company que tiver cadastrada')",
            "INSERT INTO `emoneycambio`.`configuration` (`key`, `value`, `description`) VALUES ('allowed_companies_international_shipment', 'frente-corretora|', 'Empresa que estará configurada para remessa internacional')"            
        ] 
        for sql in sqls:
            self.db_session.execute(text(sql))

    def make_commercial_coins(self):
        sqls = [
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `value`, `key`) VALUES ('Dólar Americano', 'US$', '4.97', 'USDBRL')",
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `value`, `key`) VALUES ('Dólar Canadense', 'C$', '3.71', 'CADBRL')",
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `value`, `key`) VALUES ('Bitcoin', 'B$', '150.264,20', 'BTCBRL')",
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `value`, `key`) VALUES ('Euro', '€', '5.45', 'EURBRL')",
            "INSERT INTO `emoneycambio`.`exchange_commercial_coin` (`name`, `prefix`, `value`, `key`) VALUES ('Libra esterlina', '£', '6.17', 'GBPBRL')",

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
    