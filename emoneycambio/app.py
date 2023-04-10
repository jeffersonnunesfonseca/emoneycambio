from flask import Flask
from emoneycambio import config


import logging
import sys

console = logging.StreamHandler(stream=sys.stdout)

logger_level = logging.INFO if config.LOGGER_TYPE == 'INFO' else logging.DEBUG
logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s', level=logger_level, handlers=[console])

def create_app():
    from emoneycambio.controllers import portal


    app = Flask(__name__)
    app.url_map.strict_slashes = False
    # app.config.from_object(config)
    app.register_blueprint(portal.app)
    
    return app