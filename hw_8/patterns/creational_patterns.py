import copy
import quopri

from patterns.architectural_system_patterns import DomainObject
from patterns.behavioral_patterns import ConsoleLogger


class User:
    """Абстрактный пользователь"""


class Teacher(User):
    """Преподаватель"""


class Student(User, DomainObject):
    """Студент"""
    def __init__(self, name):
        self.courses = []
        self.name = name


class UserFactory:
    """Пораждающий паттерн. Абстрактная фабрика пользователей"""
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type_, name):
        """Возвращает объект Teacher or Student. Фабричный метод"""
        return cls.types[type_](name)


class CoursePrototype:
    """Порождающий паттерн. Прототип курсов обучения"""

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    """Созание курсов"""

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    """Интерактивный курс"""
    observers = []


class RecordCourse(Course):
    """Курс в записи"""
    observers = []


class Category:
    """Категория"""
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        """Возвращает количество курсов, входящих в текущую категорию"""
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class CourseFactory:
    """Порождающий паттерн. Абстрактная фабрика курсов"""
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
    }

    @classmethod
    def create(cls, type_, name, category):
        """Возвращает курс. Фабричный метод."""
        return cls.types[type_](name, category)


class Engine:
    """Основной интерфейс проекта"""
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        """Создание юзера"""
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        """Создание категории"""
        return Category(name, category)

    @staticmethod
    def create_course(type_, name, category):
        """Создание курса"""
        return CourseFactory.create(type_, name, category)

    def find_category_by_id(self, id_):
        """Поиск категории по id"""
        for item in self.categories:
            if item.id == id_:
                return item
        raise Exception(f'Нет категории с id = {id_}')

    def get_course(self, name):
        """Получение курса"""
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name):
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace('+', ' '), 'utf8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('utf8')


class SingletonByName(type):
    """Порождающий паттерн синглтон"""
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = None
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    """Логирование"""
    def __init__(self, name, strategy=ConsoleLogger()):
        self.name = name
        self.strategy = strategy

    def log(self, text):
        text = f'log --> {text}'
        self.strategy.write_logs(text)
