from flask import Flask, redirect, request
from emoneycambio import config
from werkzeug.middleware.proxy_fix import ProxyFix


import logging
import sys

console = logging.StreamHandler(stream=sys.stdout)

logger_level = logging.INFO if config.LOGGER_TYPE == 'INFO' else logging.DEBUG
logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s', level=logger_level, handlers=[console])

LOGGER = logging.getLogger(__name__)
def create_app():
    from emoneycambio.controllers import portal
    from emoneycambio.resources.database import db
    

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2)
    app.url_map.strict_slashes = False
    
    LOGGER.info("carregando configs")
    app.config.from_object(config)
    
    LOGGER.info("carregando blueprints")
    app.register_blueprint(portal.app)
    
    LOGGER.info("carregando banco")
    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        if "remessa" in request.url:
            return redirect("/remessa-internacional", code=302)  
                 
        return redirect("/", code=302)
    
    return app
