class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE NOT FOUND'


class Framework:

    def __init__(self, routes_obj, fronts_obj):
        self.routes = routes_obj
        self.fronts = fronts_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        request = {}
        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf8')]
