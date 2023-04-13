from flask import render_template, redirect, url_for, Blueprint, jsonify, request

app = Blueprint('home', __name__)

@app.route('/', methods = ['GET'])
def index():
    # from pai_veio_monolito.services import categories

    # cat = categories.Categories()
    # data = {
    #     "title": "Hello World",
    #     "body": "A",
    #     "ads_categories": cat.get_categories_more_searches()
    # }
    data = {}
    
    return render_template('portal/home/index.html', data=data)

@app.route('/cotacao/<coin>/<location>', methods = ['GET'])
def filtered_companies(coin: str=None, location: str=None):
    from emoneycambio.services.company import Company
    if not coin or not location:
        return jsonify({"coin": coin, "location": location}), 400
    
    company = Company()
    results = company.get_companies_by_coin_and_location(coin, company)
    if not results:
        return jsonify({"coin": coin, "location": location}), 404
    
    return render_template('portal/search-result/index.html', data=results)

@app.route('/negociacao/<modality>/<type>/<coin>/<location>/<companyid>', methods = ['GET', 'POST'])
@app.route('/negociacao/<modality>/<type>/<coin>/<location>/<companyid>/<value>/<fee>', methods = ['GET', 'POST'])
def negotiation_company(modality:str=None, coin: str=None, location: str=None, type: str=None, companyid: str=None, value=None, fee=None):
    from emoneycambio.services.company import Company
    args = request.args
    json = request.get_json(silent=True)
        
    values = {
        "modality": modality, # compra / venda
        "type": type,  # papel-moeda / remessa
        "coin": coin, # moeda 
        "location": location, # local
        "companyid": companyid # idempresa
    }
    if not modality or not type or not coin or not location or not companyid:
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
        print(f"aqui enviar para o back {json}")
        # aqui salvar dados
        # import ipdb; ipdb.set_trace()
        
        
    return render_template(path_to_template, data=data, step=step)

@app.route('/remessa-internacional/', methods = ['GET'])    
@app.route('/remessa-internacional/<coin>/<person_type>/<transaction>/<value>/<fee>', methods = ['GET','POST'])
@app.route('/remessa-internacional/<coin>/<person_type>/<transaction>/<value>/<fee>/<reason>', methods = ['GET','POST'])
def remessa_internacional(coin=None, person_type=None, transaction=None, value=None, fee=None, reason=None):
    from emoneycambio.services.company import Company
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
    allowed_company = action.get_allowed_company_international_shipment() 
        
    if step != 'initial':
        path_to_template = f'portal/negotiation-international-shipment/forms/{person_type}/{transaction}/step-{step}.html'
    
    data['path_to_template']=path_to_template
    
    if json and "finish" in json:
        print(f"aqui enviar para o back {json}")
        pass
    
    if request_xhr_key and request_xhr_key == 'XMLHttpRequest':
        return render_template(path_to_template, step=step, data=data, allowed_company=allowed_company)    
    
    return render_template(path_to_template_base, step=step, data=data, allowed_company=allowed_company)