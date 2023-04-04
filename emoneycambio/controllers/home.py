from flask import render_template, redirect, url_for, Blueprint

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

# @app.route('/quero-anunciar', methods = ['GET'])
# def contact_form():
#     return render_template('home/forms/quero-anunciar.html')