from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import transaction
from fefu_lab.models import Student, Instructor, Course, Enrollment
from datetime import date
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('🧹 Очистка старых данных...')
        
        # Безопасная очистка
        try:
            Enrollment.objects.all().delete()
            Course.objects.all().delete()
            Student.objects.all().delete()
            Instructor.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Данные очищены'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️ Очистка: {e}'))

        self.stdout.write('👨‍🏫 Создание преподавателей...')
        instructors = [
            Instructor(
                first_name='Иван',
                last_name='Петров',
                email='i.petrov@fefu.ru',
                specialization='Кибербезопасность',
                degree='Кандидат технических наук',
                role='TEACHER'
            ),
            Instructor(
                first_name='Мария',
                last_name='Сидорова',
                email='m.sidorova@fefu.ru',
                specialization='Веб-разработка',
                degree='Доктор технических наук',
                role='TEACHER'
            ),
            Instructor(
                first_name='Алексей',
                last_name='Козлов',
                email='a.kozlov@fefu.ru',
                specialization='Сетевые технологии',
                role='TEACHER'
            ),
        ]
        
        for instructor in instructors:
            instructor.save()
        self.stdout.write(self.style.SUCCESS(f'✅ {len(instructors)} преподавателей'))

        self.stdout.write('👨‍🎓 Создание студентов...')
        students_data = [
            {
                'username': 'ivanov',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'email': 'ivan.ivanov@example.com',
                'birth_date': date(2000, 5, 15),
                'faculty': 'CS'
            },
            {
                'username': 'dmitrysmirnov',
                'first_name': 'Дмитрий',
                'last_name': 'Смирнов',
                'email': 'dmitry.smirnov@fefu.ru',
                'birth_date': date(1999, 8, 22),
                'faculty': 'SE'
            },
            {
                'username': 'ekaterinapopova',
                'first_name': 'Екатерина',
                'last_name': 'Попова',
                'email': 'ekaterina.popova@fefu.ru',
                'birth_date': date(2001, 3, 10),
                'faculty': 'IT'
            },
            {
                'username': 'mikhailvasilyev',
                'first_name': 'Михаил',
                'last_name': 'Васильев',
                'email': 'mikhail.vasilyev@fefu.ru',
                'birth_date': date(2000, 11, 5),
                'faculty': 'DS'
            },
            {
                'username': 'olganovikova',
                'first_name': 'Ольга',
                'last_name': 'Новикова',
                'email': 'olga.novikova@fefu.ru',
                'birth_date': date(1999, 12, 30),
                'faculty': 'WEB'
            },
        ]
        
        students = []
        for data in students_data:
            try:
                # Создаем User
                user, created = User.objects.get_or_create(
                    username=data['username'],
                    defaults={
                        'first_name': data['first_name'],
                        'last_name': data['last_name'],
                        'email': data['email'],
                        'password': 'default_password'
                    }
                )
                if not created:
                    user.set_password('default_password')
                    user.save()
                
                # Создаем Student (role не нужен в Student модели)
                student, created = Student.objects.get_or_create(
                    user=user,
                    defaults={
                        'birth_date': data['birth_date'],
                        'faculty': data['faculty']
                    }
                )
                students.append(student)
                self.stdout.write(self.style.SUCCESS(f'  ✅ {data["username"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ {data["username"]}: {e}'))

        self.stdout.write('📚 Создание курсов...')
        courses = [
            Course(
                title='Основы Python',
                slug='python-basics',
                description='Базовый курс по программированию на языке Python.',
                duration=36,
                instructor=instructors[0],
                level='BEGINNER',
                max_students=25,
                price=0
            ),
            Course(
                title='Веб-безопасность',
                slug='web-security',
                description='Продвинутый курс по защите веб-приложений.',
                duration=48,
                instructor=instructors[0],
                level='ADVANCED',
                max_students=20,
                price=15000
            ),
            Course(
                title='Современный JavaScript',
                slug='modern-javascript',
                description='Изучение ES6+, асинхронное программирование.',
                duration=42,
                instructor=instructors[1],
                level='INTERMEDIATE',
                max_students=30,
                price=12000
            ),
            Course(
                title='Защита сетей',
                slug='network-defense',
                description='Firewalls, IDS/IPS, VPN и атаки на сети.',
                duration=40,
                instructor=instructors[2],
                level='ADVANCED',
                max_students=15,
                price=18000
            ),
        ]
        
        for course in courses:
            course.save()
        self.stdout.write(self.style.SUCCESS(f'✅ {len(courses)} курсов'))

        self.stdout.write('📝 Создание записей на курсы...')
        enrollments = [
            Enrollment(student=students[0], course=courses[0], status='ACTIVE'),
            Enrollment(student=students[0], course=courses[1], status='ACTIVE'),
            Enrollment(student=students[1], course=courses[0], status='ACTIVE'),
            Enrollment(student=students[1], course=courses[2], status='ACTIVE'),
            Enrollment(student=students[2], course=courses[0], status='ACTIVE'),
            Enrollment(student=students[3], course=courses[3], status='ACTIVE'),
            Enrollment(student=students[4], course=courses[2], status='ACTIVE'),
        ]
        
        for enrollment in enrollments:
            enrollment.save()
        self.stdout.write(self.style.SUCCESS(f'✅ {len(enrollments)} записей'))

        # ✅ SUPERUSER для админки!
        self.stdout.write('🔑 Создание superuser...')
        try:
            superuser = User.objects.create_superuser(
                username='admin',
                email='admin@fefu.ru',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser: admin/admin123'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️ Superuser: {e}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Успешно создано:\n'
                f'   👨‍🏫 {len(instructors)} преподавателей\n'
                f'   👨‍🎓 {len(students)} студентов\n'
                f'   📚 {len(courses)} курсов\n'
                f'   📝 {len(enrollments)} записей\n'
                f'   🔑 admin/admin123 (админка)'
            )
        )