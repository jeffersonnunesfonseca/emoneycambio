from flask import render_template, redirect, url_for, Blueprint, jsonify, request


app = Blueprint('home', __name__)

@app.route('/', methods = ['GET'])
def index():
    data = {}
    from emoneycambio.config import PROJECT_VERSION
    
    return render_template('portal/home/index.html', data=data, version=PROJECT_VERSION)

@app.route('/cotacao/<coin>/<location>', methods = ['GET'])
def filtered_companies(coin: str=None, location: str=None):
    from emoneycambio.services.company import Company
    if not coin or not location:
        return jsonify({"coin": coin, "location": location}), 400

    company = Company()
    results = company.get_companies_by_coin_and_location(coin, location)
    
    if not results:
        return redirect("/", code=302)         
    
    return render_template('portal/search-result/index.html', data=results)

@app.route('/negociacao/<modality>/<type>/<coin>/<location>/<companybranchid>', methods = ['GET', 'POST'])
@app.route('/negociacao/<modality>/<type>/<coin>/<location>/<companybranchid>/<value>/<vet>', methods = ['GET', 'POST'])
def negotiation_company(modality:str=None, coin: str=None, location: str=None, type: str=None, companybranchid: str=None, value=None, vet=None):
    from emoneycambio.services.company import Company
    from emoneycambio.services.exchange_proposal import ExchangeProposal
    args = request.args
    json = request.get_json(silent=True)
        
    values = {
        "modality": modality, # compra / venda
        "type": type,  # papel-moeda / remessa
        "coin": coin, # moeda 
        "location": location, # local
        "companybranchid": companybranchid # idempresa
    }
    if not modality or not type or not coin or not location or not companybranchid:
        return jsonify(values), 400
    
    
    company = Company()
    data = company.get_company_to_negotiation(**values)
    if not data:
        return jsonify(values), 404
    
    step = args.get('step', '1')

    request_xhr_key = request.headers.get('X-Requested-With')
    path_to_template = 'portal/negotiation-tourism/index.html'
    if request_xhr_key and request_xhr_key == 'XMLHttpRequest':
        if args.get('step') == '3':
            path_to_template = 'portal/negotiation-tourism/forms/step-3.html'
        
        elif args.get('step') == '2':
            path_to_template = 'portal/negotiation-tourism/forms/step-2.html'
        
        elif args.get('step') == '1':
            path_to_template = 'portal/negotiation-tourism/forms/step-1.html'        

    if json and "finish" in json:
        proposal = ExchangeProposal()
        ip_addr =  request.access_route[0] if request.access_route else request.remote_addr
        headers = dict(request.headers)

        data_proposal = {            
            'company_branch_id': companybranchid,
            'company_name': data['company']['name'],
            'company_url': data['company']['url'],
            'person_type': str(json['pfpj']).upper(),
            'transaction_type': 'BUY' if modality == 'comprar' else 'SELL',
            'exchange_type': 'TOURISM',
            'reason': None,
            'total_value': value,
            'iof_fee': 0,
            'vet': vet,
            'coin_name': coin,
            'document': json['cpfcnpj'],
            'name': str(json['nome_razao_social']).capitalize(),
            'responsible_name': None,
            'email': str(json['email']).lower(),
            'phone': f"{json['ddi']}{json['phone']}",
            'phone_is_whatsapp': 1 if json.get('is_whatsapp',0) == "on" else 0,
            'delivery': 1 if json['delivery'] == 'delivery' else 0,
            'ip': ip_addr,
            'user_agent': request.user_agent,
            'headers': headers
        }
        proposal.create_exchange_proposal(**data_proposal)
        
        
    return render_template(path_to_template, data=data, step=step)

@app.route('/remessa-internacional/', methods = ['GET'])    
@app.route('/remessa-internacional/<coin>/<person_type>/<transaction>/<value>/<fee>', methods = ['GET','POST'])
@app.route('/remessa-internacional/<coin>/<person_type>/<transaction>/<value>/<fee>/<reason>', methods = ['GET','POST'])
def remessa_internacional(coin=None, person_type=None, transaction=None, value=None, fee=None, reason=None):
    
    from emoneycambio.services.company import Company
    from emoneycambio.services.exchange_proposal import ExchangeProposal
    args = request.args
    json = request.get_json(silent=True)
    
    data = {}
    request_xhr_key = request.headers.get('X-Requested-With')
    path_to_template_base = 'portal/negotiation-international-shipment/index.html'
    path_to_template= ""

    step = args.get('step', 'initial')
    if reason and not step:
        step = '2'                
    elif value and fee and not step:
        step = '1'
    
    data = {
        "coin": coin,
        "person_type": person_type,
        "transaction": transaction,
        "value": value,
        "fee": fee
    }
        
    person_type = str(data.get('person_type')).lower()
    transaction = str(data.get('transaction')).lower()   
    action = Company()
    if not coin:
        coin = args.get('coin', 'dolar-americano')     
    
    allowed_company = action.get_allowed_company_international_shipment(coin) 
    if not allowed_company:
        #  melhorar quando nao tiver
        # return jsonify({"status": "ERROR", "msg": "Moeda indisponivel no momento."})
        return redirect("/", code=302)     
        
    if step != 'initial':
        path_to_template = f'portal/negotiation-international-shipment/forms/{person_type}/{transaction}/step-{step}.html'
    
    data['path_to_template']=path_to_template
    
    if json and "finish" in json:
        proposal = ExchangeProposal()
        ip_addr =  request.access_route[0] if request.access_route else request.remote_addr
        headers = dict(request.headers)
        
        """
        {'finish': 'true', 'nextstep': '3', 'pfpj': 'pj', 'cpfcnpj': '21.211.212/2-12', 'nome_razao_social': 'Jefferson Nunes', 'nome_responsavel': 'Jefferson Nunes', 
        'email': 'jeffersonnunesfonseca@gmail.com', 'ddi': '55', 'phone': '+5541997439582', 'is_whatsapp': 'on'}
        """
        data_proposal = {            
            'company_branch_id': json['companyid'],
            'company_name': allowed_company['company']['name'],    
            'company_url': allowed_company['company']['url'],        
            'person_type': str(json['pfpj']).upper(),
            'transaction_type': 'RECEIVE' if transaction == 'receber' else 'SEND',
            'exchange_type': 'INTERNATIONAL_SHIPMENT',
            'reason': reason,
            'total_value': value,
            'iof_fee': 0,
            'vet': fee,
            'coin_name': coin,
            'document': json['cpfcnpj'],
            'name': str(json['nome_razao_social']).capitalize(),
            'responsible_name': None,
            'email': str(json['email']).lower(),
            'phone': f"{json['ddi']}{json['phone']}",
            'phone_is_whatsapp': 1 if json.get('is_whatsapp',0) == "on" else 0,
            'delivery': 0,
            'ip': ip_addr,
            'user_agent': request.user_agent,
            'headers': headers
        }
        proposal.create_exchange_proposal(**data_proposal)
    
    if request_xhr_key and request_xhr_key == 'XMLHttpRequest':
        if args.get('update_select'):
            # return allowed_company
            return render_template(path_to_template_base, step=step, data=data, allowed_company=allowed_company)    

        return render_template(path_to_template, step=step, data=data, allowed_company=allowed_company)    
    
    return render_template(path_to_template_base, step=step, data=data, allowed_company=allowed_company)


@app.route('/quem-somos/', methods = ['GET'])
def about_us():    
    return render_template('portal/about-us/index.html')

@app.route('/termos-de-uso/', methods = ['GET'])
def use_terms():    
    return render_template('portal/terms-use/index.html')

@app.route('/politicas-de-privacidade/', methods = ['GET'])
def privacy_policies():    
    return render_template('portal/privacy-policy/index.html')

@app.route('/perguntas-frequentes/', methods = ['GET'])
def faq():    
    return render_template('portal/faq/index.html')

@app.route('/fale-conosco/', methods = ['GET'])
def contact_us():    
    return render_template('portal/contact-us/index.html')

@app.route('/fale-conosco/salvar', methods = ['POST'])
def contact_us_save():    
    from emoneycambio.services.contact_us import ContactUs
    json = request.get_json(silent=True)
    json['is_whatsapp'] = 1 if json.get('is_whatsapp') else False
    print(json)
    action = ContactUs()
    try:
        response = action.create_contact_us(**json)
        if response:
            return "OK"
        raise Exception("problema ao criar contato")
    except Exception as ex:
        print(str(ex))
        return 'ERROR'
