from wsgiref.simple_server import make_server
from revike_framework.main import Framework
from urls import routes, fronts

app = Framework(routes, fronts)

with make_server('', 8000, app) as httpd:
    print('Запуск на порту 8000')
    httpd.serve_forever()
