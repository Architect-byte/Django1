from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View

STUDENTS_DATA = {
    1: {
        'info': 'Иван Петров',
        'faculty': 'Кибербезопасность',
        'status': 'Активный',
        'year': 3
    },
    2: {
        'info': 'Мария Сидорова', 
        'faculty': 'Информатика',
        'status': 'Активный',
        'year': 2
    },
    3: {
        'info': 'Алексей Козлов',
        'faculty': 'Программная инженерия', 
        'status': 'Выпускник',
        'year': 5
    }
}

COURSES_DATA = {
    'python-basics': {
        'name': 'Основы программирования на Python',
        'duration': 36,
        'description': 'Базовый курс по программированию на языке Python для начинающих.',
        'instructor': 'Доцент Петров И.С.',
        'level': 'Начальный'
    },
    'web-security': {
        'name': 'Веб-безопасность',
        'duration': 48,
        'description': 'Курс по защите веб-приложений от современных угроз.',
        'instructor': 'Профессор Сидоров А.В.',
        'level': 'Продвинутый'
    },
    'network-defense': {
        'name': 'Защита сетей',
        'duration': 42,
        'description': 'Изучение методов и технологий защиты компьютерных сетей.',
        'instructor': 'Доцент Козлова М.П.',
        'level': 'Средний'
    }
}

def home_page(request):
    #return HttpResponse("Добро пожаловать на главную страницу!")
    return render(request, 'home.html', status=200)

# def about_page(request):
#     return HttpResponse("I am dead inside")
class About_page(View):
    def get(self, request):
        #return HttpResponse("I am dead inside")
        return render(request, 'about.html', status=200)

def student_profile(request, student_id):
    if student_id in STUDENTS_DATA:
        student_data = STUDENTS_DATA[student_id]
        return render(request, 'student.html', {
            'student_id': student_id,
            'student_info': student_data['info'],
            'faculty': student_data['faculty'],
            'status': student_data['status'],
            'year': student_data['year']
        })
    else:
        raise Http404("Студент с таким ID не найден")

def course_profile(request, course_slug):
    if len(course_slug) > 20:
        return render(request, '404.html', status=404)
    context = {
        "id": course_slug
    }
    return render(request, 'course.html', status=200, context=context)

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)