-- get_companies_by_coin_and_location
select 
	(select value from configuration where `key` = 'iof_international_shipment_fee') as `default_configuration.international_shipment_iof_percentage`,
	(select value from configuration where `key` = 'iof_tourism_fee') as `default_configuration.tourism_iof_percentage`,
	cb.url_location as `filters.city.url`, 
	cb.city as `filters.city.name`, 
	cb.uf as `filters.city.uf`,
	cbec.url_coin as `filters.coin.url`, 
	cbec.name as `filters.coin.name`,
	c.id as `companies.id`,
	c.fantasy_name as `companies.name`,
	c.url as `companies.url`,
	c.logo_name as `companies.logo`,
	cb.site as `companies.site`,
	if(cbc.type!='EMAIL', cbc.value,null) as `companies.principal_phone.full_number`,
	if(cbc.type='WHATSAPP', 1,null) as `companies.principal_phone.is_whatsapp`,
	cbec.name as `companies.coin.name`,
	cbec.prefix as `companies.coin.prefix`,
	cbec.buy_tourism_vet as `companies.coin.buy_tourism_vet`,
	cbec.sell_tourism_vet as `companies.coin.sell_tourism_vet`,
	cbec.dispatch_international_shipment_vet as `companies.coin.dispatch_international_shipment_vet`,
	cbec.receipt_international_shipment_vet as `companies.coin.receipt_international_shipment_vet`,
	cbec.buy_tourism_exchange_fee as `companies.coin.buy_tourism_exchange_fee`,
	cbec.sell_tourism_exchange_fee as `companies.coin.sell_tourism_exchange_fee`,
	cbec.dispatch_international_shipment_exchange_fee as `companies.coin.dispatch_international_shipment_exchange_fee`,
	cbec.receipt_international_shipment_exchange_fee as `companies.coin.receipt_international_shipment_exchange_fee`,
	cbec.updated_at as `companies.coin.last_updated`,
	cbec.delivery as `companies.delivery.exists`,
	cbec.delivery_value as `companies.delivery.value`
from company c
inner join company_branch cb on cb.company_id = c.id
inner join company_branch_contact cbc on cbc.company_branch_id = cb.id
inner join company_branch_exchange_coin cbec on cbec.company_branch_id = cb.id
where 1=1
	and c.status = 'ENABLED'
	and cb.status = 'ENABLED' and cb.url_location = 'sao-paulo-sp'
	and cbc.status = 'ENABLED' and cbc.principal=1
	and cbec.status ='ENABLED' and cbec.url_coin = 'dolar-americano';


-- get_company_to_negotiation
select 
	(select value from configuration where `key` = 'iof_international_shipment_fee') as `default_configuration.international_shipment_iof_percentage`,
	(select value from configuration where `key` = 'iof_tourism_fee') as `default_configuration.tourism_iof_percentage`,
	cb.url_location as `filters.city.url`, 
	cb.city as `filters.city.name`, 
	cb.uf as `filters.city.uf`,
	cbec.url_coin as `filters.coin.url`, 
	cbec.name as `filters.coin.name`,
	c.id as `companies.id`,
	c.fantasy_name as `companies.name`,
	c.url as `companies.url`,
	c.logo_name as `companies.logo`,
	cb.site as `companies.site`,
	if(cbc.type!='EMAIL', cbc.value,null) as `companies.principal_phone.full_number`,
	if(cbc.type='WHATSAPP', 1,null) as `companies.principal_phone.is_whatsapp`,
	cbec.name as `companies.coin.name`,
	cbec.prefix as `companies.coin.prefix`,
	cbec.buy_tourism_vet as `companies.coin.buy_tourism_vet`,
	cbec.sell_tourism_vet as `companies.coin.sell_tourism_vet`,
	cbec.dispatch_international_shipment_vet as `companies.coin.dispatch_international_shipment_vet`,
	cbec.receipt_international_shipment_vet as `companies.coin.receipt_international_shipment_vet`,
	cbec.buy_tourism_exchange_fee as `companies.coin.buy_tourism_exchange_fee`,
	cbec.sell_tourism_exchange_fee as `companies.coin.sell_tourism_exchange_fee`,
	cbec.dispatch_international_shipment_exchange_fee as `companies.coin.dispatch_international_shipment_exchange_fee`,
	cbec.receipt_international_shipment_exchange_fee as `companies.coin.receipt_international_shipment_exchange_fee`,
	cbec.updated_at as `companies.coin.last_updated`,
	cbec.delivery as `companies.delivery.exists`,
	cbec.delivery_value as `companies.delivery.value`
from company c
inner join company_branch cb on cb.company_id = c.id
inner join company_branch_contact cbc on cbc.company_branch_id = cb.id
inner join company_branch_exchange_coin cbec on cbec.company_branch_id = cb.id
where 1=1
	and c.status = 'ENABLED'
	and cbc.status = 'ENABLED' and cbc.principal=1
	and cb.status = 'ENABLED' and cb.url_location = 'sao-paulo-sp'
	and cbec.status ='ENABLED' and cbec.url_coin = 'dolar-americano'
    and c.id = 2;