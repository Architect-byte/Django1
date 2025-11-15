from django.contrib import admin
from .models import Student, Course, Enrollment, Instructor

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'faculty', 'created_at']
    list_filter = ['faculty', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['last_name', 'first_name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'duration', 'is_active']
    list_filter = ['is_active', 'instructor']
    search_fields = ['title', 'description']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__first_name', 'student__last_name', 'course__title']

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'specialization', 'degree', 'created_at']
    list_filter = ['specialization', 'degree', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'specialization', 'degree']
    ordering = ['last_name', 'first_name']