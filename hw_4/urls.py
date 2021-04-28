from datetime import date
from views import Index, About, StudyPrograms, Courses, Category, \
    CreateCategory, CopyCourse, CreateCourse


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/study/': StudyPrograms(),
    '/courses/': Courses(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category/': Category(),
    '/copy-course/': CopyCourse()
}
