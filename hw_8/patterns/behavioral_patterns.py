import json

from revike_framework.templates import render


class Observer:
    """Наблюдатель"""
    def update(self, subject):
        pass


class Subject:
    """Подписчики"""
    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SMSNotifier(Observer):
    """СМС уведомления"""
    def update(self, subject):
        print(f'SMS: к нам присоединился {subject.students[-1].name}')


class EmailNotifier(Observer):
    """E-mail уведомления"""
    def update(self, subject):
        print(f'E-mail: к нам присоединился {subject.students[-1].name}')


class BaseSerializer:
    """Сериалайзер"""
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return json.dumps(self.obj)

    @staticmethod
    def load(data):
        return json.loads(data)


class TemplateView:
    """Шаблонный метод"""
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        return super().__call__(request)


class ConsoleLogger:
    """Вывод логов в консоль"""
    def write_logs(self, text):
        print(text)


class FileLogger:
    """Запись логов в файл"""
    def __init__(self, file):
        self.file = file

    def write_logs(self, text):
        with open(self.file, 'a', encoding='utf8') as obj:
            obj.write(f'{text}\n')
