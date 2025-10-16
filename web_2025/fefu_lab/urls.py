from django.urls import path
from . import views

handler404 = 'fefu_lab.views.custom_404_view'
handler500 = 'fefu_lab.views.custom_500_view'

urlpatterns = [
    path('', views.home_page, name='home'),  # Статический маршрут для главной страницы (/)
    path('about/', views.About_page.as_view(), name='about'),  # Статический маршрут "О нас"
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path('course/<slug:course_slug>/', views.course_profile, name='course_profile')
]