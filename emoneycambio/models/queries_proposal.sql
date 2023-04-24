SELECT 
    c.fantasy_name as empresa,
	ep.person_type as tipo_pessoa,
    ep.transaction_type as tipo_transacao,
    ep.exchange_type as tipo_turismo,
    coalesce(ep.reason, '-') as motivo,
    ep.total_value as valor_oferta,
    ep.vet as vet,
    ep.coin_name as moeda,
    ep.document as documento,
    ep.name as nome_cliente,
    coalesce(ep.responsible_name, ep.name) as nome_responsavel,
    ep.email,
    ep.phone as telefone,
    if(ep.phone_is_whatsapp=1,'whatsapp','sem_whatsapp') as whatsapp,
    if(ep.delivery=1,'delevery','sem_delivery') as delivery,
    ep.ip as ip_cliente,
    ep.user_agent,
	CASE
		WHEN ep.reason = 'pf-reason-1-send' THEN  ' Minha própria conta no exterior'
		WHEN ep.reason = 'pf-reason-2-send' THEN  'Familiar ou amigo'
		WHEN ep.reason = 'pf-reason-3-send' THEN  'Pagamento de um produto'
		WHEN ep.reason = 'pf-reason-4-send' THEN  'Pagamento de um serviço'
		WHEN ep.reason = 'pf-reason-5-send' THEN  'Investimento'
		WHEN ep.reason = 'pf-reason-1-receive' THEN  'Minha própria conta no brasil'
		WHEN ep.reason = 'pf-reason-2-receive' THEN  'Familiar ou amigo'
		WHEN ep.reason = 'pf-reason-3-receive' THEN  'Recebimento por produto vendido'
		WHEN ep.reason = 'pf-reason-4-receive' THEN  'Recebimento de serviços prestados'
		WHEN ep.reason = 'pj-reason-1-send' THEN  'Conta  da empresa no exterior'
		WHEN ep.reason = 'pj-reason-2-send' THEN  'Pagamento de um produto'
		WHEN ep.reason = 'pj-reason-3-send' THEN  'Pagamento de um serviço'
		WHEN ep.reason = 'pj-reason-4-send' THEN  'Investimento'
		WHEN ep.reason = 'pj-reason-1-receive' THEN  'Conta da empresa no brasil'
		WHEN ep.reason = 'pj-reason-2-receive' THEN  'Recebimento por produto vendido'
		WHEN ep.reason = 'pj-reason-3-receive' THEN  'Recebimento de serviços prestados'
	ELSE "-"
	END as motivo
FROM exchange_proposal ep
inner join company_branch cb on ep.company_branch_id = cb.id
inner join company c on c.id = cb.company_id
order by ep.created_at desc;

