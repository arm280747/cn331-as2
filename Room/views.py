from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Room, Booking


# Create your views here.
def home(request):
    return render(request, "room/home.html")


def allroom(request):
    #all_room = State.objects.all()
    all_room=Room.objects.all()
    return render(request, "room/available.html", {"allroom": all_room})

def selectroom1(request, room_code):
    room = get_object_or_404(Room, room_code=room_code)
    context={
        "room_code":room_code,
        "room_name":room.room_name,
        "available_hours":room.available_hours,
        "room_capacity":room.room_capacity,
        "is_available":room.is_available,
    }
    return render(request, "room/selectroom.html",context)

def addroom(request):
    room_list=Room.objects.all()
    return render(request, "room/addroom.html", {"roomlist": room_list})

def saveroom(request):
    if request.method == "POST":
        room_code = request.POST["room_code"]
        room_name = request.POST["room_name"]
        room_capacity = request.POST["room_capacity"]
        available_hours = request.POST["available_hours"]
        room_state = request.POST["room_state"]
        is_available = True

        if room_state == "True":
            is_available = True
        else:
            is_available = False

        room = Room.objects.create(
            room_code=int(room_code),
            room_name=room_name,
            room_capacity=room_capacity,
            available_hours=available_hours,
            is_available=is_available
        )
        room.save()
        return redirect("addroom")
        #print(room.room_code)

    return render(request, "room/addroom.html")

def deletepage(request):
    room_list=Room.objects.all()
    return render(request, "room/deleteroom.html", {"roomlist": room_list})

def deleteroom(request):
    if request.method == "POST":
        room_code = request.POST["room_code"]
        room = get_object_or_404(Room, room_code=room_code)
        room.delete()
        return redirect("deletepage")
    return redirect("deletepage")

def editroom(request, room_code):
    room = get_object_or_404(Room, room_code=room_code)
    if request.method == "POST":
        check_exist = Room.objects.filter(room_code=request.POST["room_code"]).exists()
        if check_exist:
            return render(request, "room/editroom.html", {"room" : room, "message" : "This room code already exist."})
        else:
            room.room_code = request.POST["room_code"]
            room.room_name = request.POST["room_name"]
            room.room_capacity = request.POST["room_capacity"]
            room.available_hours = request.POST["available_hours"]
            room_state = request.POST["room_state"]

            if room_state == "True":
                room.is_available = True
            else:
                room.is_available = False
            room.save()
            return redirect("available")
    return render(request, "room/editroom.html", {"room" : room })


# ใช้ดูห้องที่จองไว้
def mybooking(request):
    booking = Booking.objects.filter(username = request.user.username)
    return render(request, "room/mybooking.html", {"booking": booking})

def booking(request):
    if request.method == "POST":
        room_code = request.POST["room_code"]
        
        #ใช้ room__room_code = room_code เพราะ Field room เป็น FK ไปยัง Room ทำให้ Booking ไม่มี Field room_code แต่อ้างแบบนี้ได้
        check_booking = Booking.objects.filter(username = request.user.username,room__room_code=room_code)
        if not check_booking.exists():
            room = Room.objects.get(room_code=int(room_code))
            booking = Booking.objects.create(
                room=room,
                username=request.user.username
            )   
            #booking.save()
            room = get_object_or_404(Room, room_code=room_code)
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