from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("available-room/", views.allroom, name="available"),
    path("<int:room_code>/", views.room, name="room"),
    path("see-booking/", views.mybooking, name="mybooking"),
]
