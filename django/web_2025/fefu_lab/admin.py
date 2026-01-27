from django.contrib import admin
from .models import Student, Course, Enrollment, Instructor


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_last_name', 'get_first_name', 'get_email', 'faculty', 'created_at']
    list_filter = ['faculty', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    ordering = ['user__last_name', 'user__first_name']

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'
    get_first_name.short_description = 'Имя'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Фамилия'

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'duration', 'is_active']
    list_filter = ['is_active', 'instructor']
    search_fields = ['title', 'description']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'course__title']


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'specialization', 'degree', 'created_at']
    list_filter = ['specialization', 'degree', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'specialization', 'degree']
    ordering = ['last_name', 'first_name']