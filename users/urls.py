from django.urls import path


from users.apps import UsersConfig
from users.views import UserInitialization, UserAuthentication, UserProfile

app_name = UsersConfig.name

urlpatterns = [
    path('initialization/', UserInitialization.as_view(), name='initialization'),
    path('authentication/', UserAuthentication.as_view(), name='authentication'),
    path('profile/<str:phone>/', UserProfile.as_view(), name='user_profile'),
]
