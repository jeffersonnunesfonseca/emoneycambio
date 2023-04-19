import logging
__author__ = "jefferson"
__version__ = "1"
__email__ = "jeffersonnunesfonseca@gmail.com"

from emoneycambio.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5656, debug=True)    
    # io.run(app, host='0.0.0.0', port=5656, debug=True)