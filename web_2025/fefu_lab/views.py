from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View

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
    if student_id > 100:
        return render(request, '404.html', status=404)
    #return HttpResponse(f"Профиль студента с ID: {student_id}")
    context = {
        "id": student_id
    }
    return render(request, 'student.html', status=200, context=context)

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