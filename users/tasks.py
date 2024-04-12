from celery import shared_task

from users.models import User


@shared_task
def clear_auth_code(user_id):
    """Очистка поля auth_code"""
    user = User.objects.get(id=user_id)
    user.auth_code = None
    user.save()
