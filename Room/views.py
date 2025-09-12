from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import State, Room, Guest


# Create your views here.
def home(request):
    return render(request, "room/home.html")


def allroom(request):
    all_room = State.objects.all()
    return render(request, "room/available.html", {"allroom": all_room})


def room(request, room_code):
    room = get_object_or_404(Room, pk=room_code)
    return render(
        request,
        "room/room.html",
        {
            "room": room,
            "guest": room.guests.all(),
            "non_guest": Guest.objects.exclude(rooms=room).all(),
            # rooms มาจาก field ที่สร้างใน model Guest ส่วน guests มาจาก related name
        },
    )


# ใช้จองห้อง
def booking(request, room_code):
    if request.method == "POST":
        room = get_object_or_404(Room, pk=room_code)
        room_state = get_object_or_404(State, pk=room_code)
        guest = get_object_or_404(Guest, pk=int(request.POST["guest"]))
        # guest ใน method POST มาจาก name ของ input หรือ select ใน html

        if guest not in room.guests.all() and room_state.room_available():
            room_state.available_hours = room_state.available_hours - 1
            room_state.save()

            guest = Guest.objects.get(pk=int(request.POST["guest"]))
            guest.rooms.add(room)  # หรือใช้ room.guests.add(guest) ก็ได้
            guest.hours += 1
            guest.save()

            return render(
                request,
                reverse("mybooking", args=(room_state.code,)),
                {"message": "booking success"},
            )

        elif guest in room.guests.all():
            return render(
                request,
                reverse("room", args=(room_state.code,)),
                {"message": "You're already book this room"},
            )
        else:
            return render(
                request,
                reverse("room", args=(room_state.code,)),
                {"message": "This room is full"},
            )

    return render(
        request, reverse("home"), {"message": "some error occur please try again"}
    )


# ใช้ดูห้องที่จองไว้
def mybooking(request):
    booking = Room.objects.filter(room_name=request.user)
    return render(request, "room/mybooking.html", {"booking": booking})
