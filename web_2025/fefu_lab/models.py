from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Instructor(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'Студент'),
        ('TEACHER', 'Преподаватель'),
        ('ADMIN', 'Админ'),
    ]
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    specialization = models.CharField(max_length=200, blank=True, verbose_name='Специализация')
    degree = models.CharField(max_length=200, blank=True, verbose_name='Учёная степень')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='TEACHER', verbose_name='Роль')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Student(models.Model):
    FACULTY_CHOICES = [
        ('CS', 'Кибербезопасность'),
        ('SE', 'Программная инженерия'),
        ('IT', 'Информационные технологии'),
        ('DS', 'Наука о данных'),
        ('WEB', 'Веб-технологии'),
    ]
    ROLE_CHOICES = [
        ('STUDENT', 'Студент'),
        ('TEACHER', 'Преподаватель'),
        ('ADMIN', 'Админ'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Пользователь'
    )

    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    faculty = models.CharField(max_length=3, choices=FACULTY_CHOICES, default='CS', verbose_name='Факультет')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT', verbose_name='Роль')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Course(models.Model):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Начальный'),
        ('INTERMEDIATE', 'Средний'),
        ('ADVANCED', 'Продвинутый'),
    ]

    title = models.CharField(max_length=200, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')
    duration = models.PositiveIntegerField(verbose_name='Продолжительность (часы)')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Преподаватель')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='BEGINNER', verbose_name='Уровень')
    max_students = models.PositiveIntegerField(default=0, verbose_name='Максимальное количество студентов')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Активен'),
        ('COMPLETED', 'Завершен'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments', verbose_name='Студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='Курс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='Статус')

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} - {self.course} ({self.status})"