from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.login_views, name="Login"),
    path("logout/", views.logout_views, name="Logout"),
    path("home/", views.index, name="home"),
    path("register/", views.register_views, name="Register"),
]
