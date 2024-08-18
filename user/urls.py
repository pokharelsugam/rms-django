from django.urls import path
from user.views import user_management, login_universal, register_universal, logout_universal, profile

urlpatterns = [
    path('', user_management, name = 'user_management'),
    path('login/', login_universal, name = 'login_universal'),
    path('profile/', profile, name = 'profile'),
    path('register/', register_universal, name='register_universal'),
    path('logout/', logout_universal, name='logout_universal'),
]
