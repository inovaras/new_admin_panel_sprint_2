def hello(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain, charset=utf-8')])
    yield 'Hello PRACTIKUM!\n'.encode('utf-8')
