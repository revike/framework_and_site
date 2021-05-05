from wsgiref.simple_server import make_server
from revike_framework.main import Framework
from urls import fronts
from views import routes

app = Framework(routes, fronts)

with make_server('', 8000, app) as httpd:
    print('Запуск на порту 8000')
    print(f'http://127.0.0.1:8000')
    httpd.serve_forever()
