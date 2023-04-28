from flask import Flask, redirect, request, render_template
# from flask_socketio import SocketIO, emit, send

from emoneycambio import config
from werkzeug.middleware.proxy_fix import ProxyFix
import json

import logging
import sys

from threading import Lock
thread = None
thread_lock = Lock()


console = logging.StreamHandler(stream=sys.stdout)

logger_level = logging.INFO if config.LOGGER_TYPE == 'INFO' else logging.DEBUG
logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s', level=logger_level, handlers=[console])

LOGGER = logging.getLogger(__name__)
# def create_app():
from emoneycambio.controllers import portal
from emoneycambio.apis import exchange_commercial_coin
from emoneycambio.resources.database import db


app = Flask(__name__)
# io = SocketIO(app, async_mode=None)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2)
app.url_map.strict_slashes = False

LOGGER.info("carregando configs")
app.config.from_object(config)



# def background_thread():
#     """Example of how to send server generated events to clients."""
#     # with app.app_context() as apps:
#     while True:
#         from emoneycambio.services.exchange_commercial_coin import ExchangeCommercialCoin
#         action = ExchangeCommercialCoin()        
#         coins = action.get_updated_coins()
#         io.emit('getMessage', json.dumps(coins))
#         io.sleep(10)
        
# @io.on('update_commercial_exchange')
# def handle_commercial_exchange(msg):
#     global thread
#     from emoneycambio.services.exchange_commercial_coin import ExchangeCommercialCoin
#     action = ExchangeCommercialCoin()        
#     coins = action.get_updated_coins()
#     io.emit('getMessage', json.dumps(coins))
#     with thread_lock:
#         if thread is None:
#             thread = io.start_background_task(background_thread)
    # io.emit('getMessage', json.dumps(coins))

    
LOGGER.info("carregando blueprints")

app.register_blueprint(portal.app)
app.register_blueprint(exchange_commercial_coin.api)

LOGGER.info("carregando banco")
db.init_app(app)

@app.errorhandler(404)
def page_not_found(e):
    if "remessa" in request.url:
        return redirect("/remessa-internacional", code=302)  
                
    return render_template('portal/error.html'), 404
       