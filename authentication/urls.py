from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('permission', views.permission, name="permission"),
    path('signout', views.signout, name="signout"),
    path('successful', views.successful, name="successful"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('check_email', views.check_email, name="check_email"),
]
