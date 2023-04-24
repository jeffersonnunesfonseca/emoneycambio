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
    ep.user_agent 
    
FROM exchange_proposal ep
inner join company_branch cb on ep.company_branch_id = cb.id
inner join company c on c.id = cb.company_id
order by ep.created_at desc
;


truncate exchange_proposal;