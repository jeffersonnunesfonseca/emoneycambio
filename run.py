import logging
__author__ = "jefferson"
__version__ = "1"
__email__ = "jeffersonnunesfonseca@gmail.com"

from emoneycambio.app import app, io
import eventlet
eventlet.monkey_patch()

# run = app.create_app()
# io = app.socket_io()


if __name__ == '__main__':
    # run.run(host='0.0.0.0', port=5656, debug=True)
    
    io.run(app, host='0.0.0.0', port=5656, debug=True)