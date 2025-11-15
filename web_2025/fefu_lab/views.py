from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.models import User
from .form import LoginForm, RegistrationForm, FeedbackForm
from .models import Student, Course, Instructor


def home_page(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_instructors = Instructor.objects.count()
    recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
    return render(request, 'home.html', {
        'title': 'Главная страница',
        'total_students': total_students,
        'total_courses': total_courses,
        'total_instructors': total_instructors,
        'recent_courses': recent_courses
    })


def student_profile(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    other_students = Student.objects.exclude(pk=student_id)[:10]  # например, 10 других студентов
    return render(request, 'student.html', {
        'student': student,
        'other_students': other_students,
        'title': f'Профиль студента {student.first_name}',
    })


def course_profile(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    other_courses = Course.objects.exclude(pk=course.pk)[:10]
    return render(request, 'course.html', {
        'course': course,
        'other_courses': other_courses,
        'title': f'Детали курса {course.slug}'
    })

def course_list(request):
    courses = Course.objects.all().order_by('id')  # Список всех курсов по возрастанию id
    return render(request, 'course_list.html', {
        'courses': courses,
        'title': 'Список курсов',
    })


class About_page(View):
    def get(self, request):
        return render(request, 'about.html', status=200)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'success.html', {
                'message': 'Вход выполнен успешно! Добро пожаловать в систему.',
                'title': 'Вход в систему'
            })
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'title': 'Вход в систему'})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            # Создаем связанного студента
            Student.objects.create(
                first_name=username,
                last_name='Маркс',
                email=email,
                faculty='CS'
            )
            return render(request, 'success.html', {
                'message': 'Регистрация прошла успешно! Теперь вы можете войти в систему.',
                'title': 'Регистрация успешна'
            })
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form, 'title': 'Регистрация'})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            return render(request, 'success.html', {
                'message': 'Спасибо за ваш отзыв!',
                'title': 'Отзыв получен'
            })
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form, 'title': 'Обратная связь'})


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)