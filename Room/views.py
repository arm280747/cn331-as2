from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import State, Room, Guest, Booking


# Create your views here.
def home(request):
    return render(request, "room/home.html")


def allroom(request):
    #all_room = State.objects.all()
    all_room=Room.objects.all()
    return render(request, "room/available.html", {"allroom": all_room})


def selectroom(request):
    room_code=request.GET.get('id')
    room = get_object_or_404(Room, pk=room_code)
    return render(
        request,
        "room/selectroom.html",
        {
            "room": room,
            "guest": room.guests.all(),
            "non_guest": Guest.objects.exclude(rooms=room).all(),
            # rooms มาจาก field ที่สร้างใน model Guest ส่วน guests มาจาก related name
        },
    )

def selectroom1(request):
    room_code=request.GET.get('id')
    room = get_object_or_404(Room, pk=room_code)
    context={
        "room_code":room_code,
        "room_name":room.room_name,
        "available_hours":room.available_hours,
        "room_capacity":room.room_capacity
    }
    return render(request, "room/selectroom.html",context)

# ใช้จองห้อง
def booking_test(request, room_code):
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

def addroom(request):
    room_list=Room.objects.all()
    return render(request, "room/addroom.html", {"roomlist": room_list})
def saveroom(request):
    if request.method == "POST":
        room_code = request.POST["room_code"]
        room_name = request.POST["room_name"]
        room_capacity = request.POST["room_capacity"]
        available_hours = request.POST["available_hours"]
        is_available = True
        room = Room.objects.create(
            room_code=int(room_code),
            room_name=room_name,
            room_capacity=room_capacity,
            available_hours=available_hours,
            is_available=True
        )
        room.save()
        return redirect("addroom")
        #print(room.room_code)

    return render(request, "room/addroom.html")

# ใช้ดูห้องที่จองไว้
def mybooking(request):
    booking = Booking.objects.filter(username = request.user.username)
    return render(request, "room/mybooking.html", {"booking": booking})

def booking(request):
    if request.method == "POST":
        room_code = request.POST["room_code"]
        
        check_booking = Booking.objects.filter(username = request.user.username,room_code=room_code)
        if not check_booking.exists():
            booking = Booking.objects.create(
                room_code=int(room_code),
                username=request.user.username
            )   
            #booking.save()
            room = get_object_or_404(Room, pk=room_code)
            if room.available_hours>0:
                room.available_hours -= 1
                room.save()
        return redirect("home")
        #print(room.room_code)

    return render(request, "room/home.html")

def cancel(request):
    id=request.GET.get('id')
    booking=Booking.objects.get(pk=id)
    booking.delete()
    room = get_object_or_404(Room, pk=booking.room_code)
    if room.available_hours>0:
        room.available_hours += 1
        room.save()
    return render(request,"room/home.html")