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
def negotiation_company(modality:str=None, coin: str=None, location: str=None, type: str=None, companyid: str=None):
    from emoneycambio.services.company import Company
    args = request.args
    json = request.get_json(silent=True)
    print(json)
        
    values = {
        "modality": modality,
        "type": type, 
        "coin": coin, 
        "location": location, 
        "companyid": companyid
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
            # return render_template('portal/negotiation-tourism/forms/step-3.html', data=data, step=step)
        
        elif args.get('step') == '2':
            path_to_template = 'portal/negotiation-tourism/forms/step-2.html'
            # return render_template('portal/negotiation-tourism/forms/step-2.html', data=data, step=step)
        
        elif args.get('step') == '1':
            path_to_template = 'portal/negotiation-tourism/forms/step-1.html'
            # return render_template('portal/negotiation-tourism/forms/step-1.html', data=data, step=step)
        
        
    return render_template(path_to_template, data=data, step=step)
    
@app.route('/remessa-internacional', methods = ['GET'])
def remessa_internacional():
    
    return render_template('portal/negotiation-international-shipment/index.html')