from datetime import date

from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from revike_framework.templates import render

site = Engine()
logger = Logger('main')
routes = {}


@AppRoute(routes, '/')
class Index:
    """Главная страница"""
    @Debug('Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes, '/about/')
class About:
    """О проекте"""
    @Debug('About')
    def __call__(self, request):
        return '200 OK', render('about.html')


class NotFound404:
    """Error 404"""
    @Debug('NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes, '/study/')
class StudyPrograms:
    """Расписания"""
    @Debug('StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study.html', data=date.today())


@AppRoute(routes, '/courses/')
class Courses:
    """Список курсов"""
    @Debug('Courses')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render(
                'courses.html', objects_list=category.courses,
                name=category.name, id=category.id
            )
        except KeyError:
            return '200 OK', 'Курсы еще не добавлены'

@AppRoute(routes, '/category/')
class Category:
    """список категорий"""
    @Debug('Category')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category.html', objects_list=site.categories)


@AppRoute(routes, '/create-course/')
class CreateCourse:
    """Создание курсов"""
    category_id = -1
    @Debug('CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            name = site.decode_value(request['data']['name'])
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                site.courses.append(course)
            return '200 OK', render(
                'courses.html', objects_list=category.courses,
                name=category.name, id=category.id
            )
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                return '200 OK', render(
                    'create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'Категории еще не добавлены'


@AppRoute(routes, '/create-category/')
class CreateCategory:
    """Создание категории"""
    @Debug('CreateCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = site.decode_value(data['name'])
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render(
                'create_category.html', categories=categories
            )


@AppRoute(routes, '/copy-course/')
class CopyCourse:
    """Копирование курсов"""
    @Debug('CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
            return '200 OK', render('courses.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'Курсы еще не добавлены'
