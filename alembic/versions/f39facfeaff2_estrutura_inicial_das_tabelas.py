"""estrutura inicial das tabelas

Revision ID: f39facfeaff2
Revises: 
Create Date: 2023-04-17 14:04:06.736751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f39facfeaff2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    
    company()
    company_branch()
    company_branch_contact()
    company_branch_exchange_coin()
    company_branch_exchange_coin_history()
    exchange_commercial_coin()
    exchange_commercial_coin_history()
    exchange_proposal()
    lead_distribution_event()
    configuration()

def downgrade():
    op.execute("DROP TABLE configuration")
    op.execute("DROP TABLE lead_distribution_event")
    op.execute("DROP TABLE exchange_proposal")
    op.execute("DROP TABLE exchange_commercial_coin_history")
    op.execute("DROP TABLE exchange_commercial_coin")
    op.execute("DROP TABLE company_branch_exchange_coin_history")
    op.execute("DROP TABLE company_branch_exchange_coin")
    op.execute("DROP TABLE company_branch_contact")
    op.execute("DROP TABLE company_branch")
    op.execute("DROP TABLE company")

def company():
    """Empresas cadastradas"""
    sql = """
    CREATE TABLE IF NOT EXISTS `company` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `cnpj` VARCHAR(14) NOT NULL,
    `name` VARCHAR(150) NOT NULL,
    `fantasy_name` VARCHAR(100) NULL,
    `url` VARCHAR(150) NOT NULL,
    `logo_name` VARCHAR(150) NULL,
    `status` ENUM('ENABLED', 'DISABLED') NULL DEFAULT 'ENABLED',
    `created_at` DATETIME NULL DEFAULT now(),
    `updated_at` DATETIME NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `company_cnpj_UNIQUE` (`cnpj` ASC),
    INDEX `company_cnpj` (`cnpj` ASC),
    INDEX `company_created_at_status` (`created_at` ASC, `status` ASC),
    INDEX `company_updated_at_status` (`updated_at` ASC, `status` ASC))"""
    
    op.execute(sql)

def company_branch():
    """FIliais da empresa, facilita quando a empresa tem mais de uma loja, se existir somente uma ou se a principal 
    também existir o campo 'principal' deve ser True"""
    sql = """
    CREATE TABLE IF NOT EXISTS `company_branch` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `company_id` INT NULL,
    `principal` TINYINT NOT NULL DEFAULT 1,
    `name` VARCHAR(150) NOT NULL,
    `site` VARCHAR(200) NULL,
    `full_address` VARCHAR(350) NULL,
    `complement` VARCHAR(150) NULL,
    `uf` VARCHAR(2) NOT NULL,
    `city` VARCHAR(150) NOT NULL,
    `url_location` VARCHAR(150) NOT NULL,
    `cep` VARCHAR(8),
    `coordinates` GEOMETRY NULL,
    `status` ENUM('ENABLED', 'DISABLED') NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT now(),
    `updated_at` DATETIME NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_company_branch_company_id` (`company_id` ASC),
    INDEX `idx_url_location` (`url_location` ASC),    
    INDEX `idx_company_branch_created_at_status` (`created_at` ASC, `status` ASC),
    INDEX `idx_company_branch_updated_at_status` (`status` ASC, `updated_at` ASC),
    INDEX `idx_company_branch_uf` (`uf` ASC),
    INDEX `idx_company_branch_city` (`city` ASC),
    CONSTRAINT `fk_company_branch_company_id`
        FOREIGN KEY (`company_id`)
        REFERENCES `company` (`id`))"""
    op.execute(sql)

def company_branch_contact():
    """Contatos das filiais, o principal contato deverá estar marcado com o principal =1 e só pode existir 
    1 principal para cada type"""
    
    sql = """
    CREATE TABLE IF NOT EXISTS `company_branch_contact` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `company_branch_id` INT NOT NULL,
    `type` ENUM('PHONE', 'CELLPHONE', 'WHATSAPP', 'EMAIL') NOT NULL,
    `principal` TINYINT NOT NULL DEFAULT 1,
    `value` VARCHAR(200) NOT NULL,
    `status` ENUM('ENABLED', 'DISABLED') NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT now(),
    `updated_at` DATETIME NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_company_branch_contact_created_at_status` (`created_at` ASC, `status` ASC),
    INDEX `idx_company_branch_contact_updated_at_status` (`status` ASC, `updated_at` ASC),
    INDEX `fk_company_branch_contact_company_branch_id_idx` (`company_branch_id` ASC),
    INDEX `idx_company_branch_contact_type` (`type` ASC),
    INDEX `idx_company_branch_contact_value` (`value` ASC),
    CONSTRAINT `fk_company_branch_contact_company_branch_id`
        FOREIGN KEY (`company_branch_id`)
        REFERENCES `company_branch` (`id`))"""
    op.execute(sql)

def company_branch_exchange_coin():
    """Moedas que a filial vende"""
    sql = """
    CREATE TABLE IF NOT EXISTS `company_branch_exchange_coin` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `company_branch_id` INT NOT NULL,
    `name` VARCHAR(150) NOT NULL,
    `url_coin` VARCHAR(150) NOT NULL,
    `prefix` VARCHAR(10) NULL,
    `status` ENUM('ENABLED', 'DISABLED') NOT NULL,
    `buy_tourism_vet` DECIMAL(17,5),
    `sell_tourism_vet` DECIMAL(17,5),
    `dispatch_international_shipment_vet` DECIMAL(17,5),
    `receipt_international_shipment_vet` DECIMAL(17,5),
    `buy_tourism_exchange_fee` DECIMAL(17,5),
    `sell_tourism_exchange_fee` DECIMAL(17,5),
    `dispatch_international_shipment_exchange_fee` DECIMAL(17,5),
    `receipt_international_shipment_exchange_fee` DECIMAL(17,5),
    `delivery` TINYINT NOT NULL DEFAULT 0,
    `delivery_value` DECIMAL(17,5),
    `created_at` DATETIME NOT NULL DEFAULT now(),
    `updated_at` DATETIME NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_company_branch_exchange_coin_created_at_status` (`created_at` ASC, `status` ASC),
    INDEX `idx_company_branch_exchange_coin_updated_at_status` (`status` ASC, `updated_at` ASC),
    INDEX `idx_url_coin` (`url_coin` ASC),
    INDEX `fk_company_branch_exchange_coin_company_branch_id_idx` (`company_branch_id` ASC),
    INDEX `idx_company_branch_exchange_coin_prefix` (`prefix` ASC),
    CONSTRAINT `fk_company_branch_exchange_coin_company_branch_id`
        FOREIGN KEY (`company_branch_id`)
        REFERENCES `company_branch` (`id`))"""
    op.execute(sql)

def company_branch_exchange_coin_history():
    """Mantém histórico de valores da moeda que a filial esta vendendo/comprando"""
    sql = """
    CREATE TABLE IF NOT EXISTS `company_branch_exchange_coin_history` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `company_branch_exchange_coin_id` INT NOT NULL,
    `buy_tourism_vet` DECIMAL(17,5),
    `sell_tourism_vet` DECIMAL(17,5),
    `dispatch_international_shipment_vet` DECIMAL(17,5),
    `receipt_international_shipment_vet` DECIMAL(17,5),
    `buy_tourism_exchange_fee` DECIMAL(17,5),
    `sell_tourism_exchange_fee` DECIMAL(17,5),
    `dispatch_international_shipment_exchange_fee` DECIMAL(17,5),
    `receipt_international_shipment_exchange_fee` DECIMAL(17,5),
    `iof_tourism_fee` DECIMAL(17,5) NOT NULL,
    `iof_international_shipment_fee` DECIMAL(17,5) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT now(),
    PRIMARY KEY (`id`),
    INDEX `idx_company_branch_exchange_coin_history_created_at_status` (`created_at` ASC),
    INDEX `idx_company_branch_exchange_coin` (`company_branch_exchange_coin_id` ASC),
    CONSTRAINT `fk_company_branch_exchange_coin`
        FOREIGN KEY (`company_branch_exchange_coin_id`)
        REFERENCES `company_branch_exchange_coin` (`id`))"""
    op.execute(sql)

def exchange_commercial_coin():
    """Valor das moedas, tabela será atualizada com muita frequencia"""
    sql = """
    CREATE TABLE IF NOT EXISTS `exchange_commercial_coin` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(150) NOT NULL,
    `key` VARCHAR(150) NOT NULL,
    `prefix` VARCHAR(10) NULL,
    `value` DECIMAL(17,5) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT now(),
    `updated_at` DATETIME NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_exchange_commercial_coin_created_at` (`created_at` ASC),
    INDEX `idx_exchange_commercial_coin_updated_at` (`updated_at` ASC),
    INDEX `idx_exchange_commercial_coin_key` (`key` ASC),
    INDEX `idx_exchange_commercial_coin_prefix` (`prefix` ASC))"""
    op.execute(sql)

def exchange_commercial_coin_history():
    """Histórico das moedas comerciais"""
    sql = """
    CREATE TABLE IF NOT EXISTS `exchange_commercial_coin_history` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `exchange_commercial_coin_id` INT NOT NULL,
    `value` DECIMAL(17,5) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT now(),

    PRIMARY KEY (`id`),
    INDEX `idx_exchange_commercial_coin_history_created_at_status` (`created_at` ASC),
    INDEX `idx_exchange_commercial_coin_history_prefix` (`exchange_commercial_coin_id` ASC),
    UNIQUE KEY `uq_exchange_commercial_coin_id_value` (`exchange_commercial_coin_id`,`value`),
    CONSTRAINT `fk_exchange_commercial_coin_history_exchange_commercial_coin_id`
        FOREIGN KEY (`exchange_commercial_coin_id`)
        REFERENCES `exchange_commercial_coin` (`id`))"""
    op.execute(sql)

def exchange_proposal():
    """Propostas que os clientes realizam por filial"""
    sql = """
    CREATE TABLE IF NOT EXISTS `exchange_proposal` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `company_branch_id` INT NOT NULL,
    `person_type` ENUM('PF', 'PJ') NOT NULL,
    `transaction_type` ENUM('BUY', 'SELL', 'SEND', 'RECEIVE') NOT NULL,
    `exchange_type` ENUM('TOURISM', 'INTERNATIONAL_SHIPMENT') NOT NULL,
    `reason` VARCHAR(100) NULL,
    `total_value` DECIMAL(17,5) NOT NULL,
    `iof_fee` DECIMAL(17,5) NOT NULL,
    `vet` DECIMAL(17,5) NOT NULL,
    `coin_name` VARCHAR(150) NOT NULL,
    `document` VARCHAR(14) NULL,
    `name` VARCHAR(150) NOT NULL,
    `responsible_name` VARCHAR(150) NULL,
    `email` VARCHAR(150) NOT NULL,
    `phone` VARCHAR(13) NOT NULL,
    `phone_is_whatsapp` TINYINT NOT NULL DEFAULT 1,
    `delivery` TINYINT NOT NULL DEFAULT 0,
    `ip` VARCHAR(200) NOT NULL,
    `user_agent` TEXT NOT NULL,
    `headers` TEXT NOT NULL,    
    `created_at` DATETIME NULL DEFAULT now(),
    PRIMARY KEY (`id`),
    INDEX `idx_exchange_proposal_created_at_status` (`created_at` ASC),
    INDEX `fk_exchange_proposal_company_branch_id_idx` (`company_branch_id` ASC),
    INDEX `uq_exchange_proposal_proposal` (`company_branch_id` ASC, `person_type` ASC, `transaction_type` ASC, `exchange_type` ASC, `reason` ASC, `document` ASC, `phone` ASC, `email` ASC),
    CONSTRAINT `fk_exchange_proposal_company_branch_id0`
        FOREIGN KEY (`company_branch_id`)
        REFERENCES `company_branch` (`id`))"""
    op.execute(sql)

def lead_distribution_event():
    """Registro de distribuição dos leads"""
    sql = """
        CREATE TABLE IF NOT EXISTS `lead_distribution_event` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `company_branch_id` INT NOT NULL,
    `origin_company_branch_id` INT NULL,
    `channel` ENUM('EMAIL', 'SMS', 'WHATSAPP', 'PARTNER_REGISTER') NOT NULL,
    `product_type` ENUM('EXCHANGE_PROPOSAL', 'LOAN_PROPOSAL') NOT NULL,
    `relationship_id` INT NULL,
    `created_at` DATETIME NOT NULL DEFAULT now(),
    `updated_at` DATETIME NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_lead_distribution_event_created_at` (`created_at` ASC),
    INDEX `idx_lead_distribution_event_updated` (`updated_at` ASC),
    INDEX `idx_lead_distribution_event_channel` (`channel` ASC),
    INDEX `idx_lead_distribution_event_type` (`product_type` ASC),
    CONSTRAINT `fk_lead_distribution_event_exchange_commercial_coin_id`
        FOREIGN KEY (`company_branch_id`)
        REFERENCES `company_branch` (`id`))"""
    op.execute(sql)

def configuration():
    """Configurações dinamicas"""
    sql = """
    CREATE TABLE IF NOT EXISTS `configuration` (
    `key` VARCHAR(255) NOT NULL,
    `value` VARCHAR(255) NULL,
    `description` VARCHAR(255) NULL,
    `created_at` DATETIME NULL DEFAULT now(),
    `updated_at` DATETIME NULL,
    PRIMARY KEY (`key`))"""
    op.execute(sql)

