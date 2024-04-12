import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=150, unique=True, verbose_name='почта', **NULLABLE)
    auth_code = models.CharField(max_length=128, **NULLABLE)
    invite_code = models.CharField(max_length=6, unique=True, verbose_name='Код для приглашения', **NULLABLE)
    activated_invite_code = models.CharField(max_length=6, verbose_name='активируемый код приглашения', **NULLABLE)
    invited_users = models.ManyToManyField('self', symmetrical=False, **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


