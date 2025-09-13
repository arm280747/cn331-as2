from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("available-room/", views.allroom, name="available"),
    #path("selectroom/<int:room_code>", views.room, name="selectroom"),
    path("selectroom/", views.selectroom, name="selectroom"),
    path("see-booking/", views.mybooking, name="mybooking"),
    path("addroom/", views.addroom, name="addroom"),
    path("saveroom/", views.saveroom, name="saveroom"),
    path("booking/", views.booking, name="booking"),
    path("cancel/", views.cancel, name="cancel"),
]
