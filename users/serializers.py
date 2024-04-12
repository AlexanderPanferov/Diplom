import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User



class UserCreateSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

    def validate_phone(self, value):
        """
        Проверка номера телефона на соответствие
        """
        if not re.match(r'^89\d{9}$', value):
            raise ValidationError("Номер телефона должен быть в формате 89XXXXXXXXX")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone', 'email', 'invite_code', 'activated_invite_code', 'invited_users')

    def validate(self, data):
        """
        Проверяем, что новый код не пытаются установить, если уже есть активированный и
        что введенный инвайт-код существует
        """
        activated_invite_code = data.get('activated_invite_code')

        if self.instance and self.instance.activated_invite_code and activated_invite_code:
            if self.instance.activated_invite_code != activated_invite_code:
                raise ValidationError({"Активация": "Нельзя изменить существующий код приглашения!"})

        if activated_invite_code and not User.objects.filter(invite_code=activated_invite_code).exists():
            raise ValidationError({"Активация": "Введенный код приглашения не существует!"})

        return data

    def get_invited_users(self, obj):
        return User.objects.filter(activated_invite_code=obj.invite_code).values_list('phone', flat=True)
