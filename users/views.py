from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsOwner
from .serializers import UserCreateSerializer, UserProfileSerializer
from django.utils import timezone

from .services import code_generation
from .tasks import clear_auth_code


class UserInitialization(generics.CreateAPIView):
    """Первичная регистрация и получение кода для регистрации и авторизации"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            hashed_code = make_password(code_generation())
            user, created = User.objects.update_or_create(
                phone=phone,
                defaults={'auth_code': hashed_code},
            )
            # Запуск задачи для очистки кода доступа по соображениям безопасности
            clear_auth_code.apply_async((user.id,), eta=timezone.now() + timedelta(minutes=2))

            return Response({'Код отправлен'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthentication(APIView):
    """Аунтификация пользователя"""

    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        try:
            user = User.objects.get(phone=phone)
            if check_password(code, user.auth_code):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'Пользователя с таким номером не существует'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    """Запрос профиля пользователя и изменение данных профиля"""
    permission_classes = [IsOwner]

    def get(self, request, phone):
        user = User.objects.get(phone=phone)
        self.check_object_permissions(request, user)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request, phone):
        user = get_object_or_404(User, phone=phone)
        self.check_object_permissions(request, user)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
