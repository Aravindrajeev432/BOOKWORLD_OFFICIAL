
from django.urls import path
from . import views
urlpatterns = [
    path('login', views.user_login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    # path('user',include('bookworld.urls')),
    path('otp_verification_send', views.otp_verfication_send,
         name="otp_verification_send"),
    path('otp_verification_check/<int:Phone_number>/',
         views.otp_verification_check, name='otp_verification_check'),
]
