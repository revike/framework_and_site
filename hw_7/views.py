from datetime import date

from patterns.behavioral_patterns import EmailNotifier, SMSNotifier, \
    BaseSerializer, ListView, CreateView
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from revike_framework.templates import render

site = Engine()
logger = Logger('main')
routes = {}
email_notifier = EmailNotifier()
sms_notifier = SMSNotifier()


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
    """Список категорий"""

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
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
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


@AppRoute(routes=routes, url='/student/')
class StudentListview(ListView):
    """Просмотр студентов"""
    queryset = site.students
    template_name = 'student.html'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    """Создание студентов"""
    template_name = 'create_student.html'

    def create_obj(self, data):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentCreateView(CreateView):
    """Добавление студентов на курсы"""
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)

        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        # course.add_student(student)
        print(f'Добавляем студента {student_name} на курс - {course_name}')


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
