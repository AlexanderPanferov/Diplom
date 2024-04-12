from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание супер пользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(
            phone='89999999999',
            email='admin@admin.admin',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('Qwer4321')
        user.save()