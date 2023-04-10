import multiprocessing

bind = '0.0.0.0:5656'

workers = multiprocessing.cpu_count()

worker_class = 'eventlet'

timeout = 60 * 8

loglevel = 'info'