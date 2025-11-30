from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Instructor

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Попытка аутентификации через User с паролем
        if email and password:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                pass

        # Если пароль не передан или User не найден,
        # проверяем есть ли Instructor с таким email (без пароля, только по email)
        if email:
            try:
                instructor = Instructor.objects.get(email=email)
                # Создадим или получим временного User без пароля для сессии
                user, created = User.objects.get_or_create(
                    username=f"instructor_{instructor.id}",
                    defaults={
                        'first_name': instructor.first_name,
                        'last_name': instructor.last_name,
                        'email': instructor.email,
                        'password': 'default_password'  # пустой, чтобы не залогиниться по паролю
                    }
                )
                return user
            except Instructor.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None