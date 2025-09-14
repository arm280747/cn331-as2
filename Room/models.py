from django.db import models


# Create your models here.
class Room(models.Model):
    room_code = models.IntegerField(unique=True)
    room_name = models.CharField(max_length=200)
    room_capacity = models.IntegerField()
    available_hours = models.IntegerField(default=24)
    is_available = models.BooleanField(default=True)

    # self คือตัวแทนของ object ที่ถูกสร้างขึ้นจาก class นั้นๆ
    def __str__(self):
        return f"{self.room_name} ({self.room_code})"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    date_booking = models.DateTimeField(auto_now_add=True)

    # self คือตัวแทนของ object ที่ถูกสร้างขึ้นจาก class นั้นๆ
    def __str__(self):
        return f"{self.username} ({self.room.room_code})"
