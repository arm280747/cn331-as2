from django.db import models


# Create your models here.
class Room(models.Model):
    room_code = models.IntegerField(primary_key=True)
    room_name = models.CharField(max_length=200)
    room_capacity = models.IntegerField()

    # self คือตัวแทนของ object ที่ถูกสร้างขึ้นจาก class นั้นๆ
    def __str__(self):
        return f"{self.room_name} ({self.room_code})"


class State(models.Model):
    # ใช้ OneToOne เพราะคิดว่า 1 ห้องไม่น่ามีชั่วโมงว่างกับสถานะเปิดให้จองหลายตัว
    code = models.OneToOneField(Room, on_delete=models.CASCADE, related_name="Code")
    name = models.OneToOneField(Room, on_delete=models.CASCADE, related_name="Name")
    capacity = models.OneToOneField(
        Room, on_delete=models.CASCADE, related_name="Capacity"
    )
    available_hours = models.IntegerField(default=24)
    room_state = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code}: {self.name} Status:{self.room_state}"

    def room_available(self):
        return (self.available_hours >= 1) and (self.room_state)

    # function ใช้เปลี่ยน state เมื่อจำนวนชั่วโมงว่างน้อยกว่า 1
    def save_state_change(self, *arg, **kwargs):
        if self.available_hours < 1:
            self.room_state = False
        else:
            self.room_state = True
        super().save(*arg, **kwargs)  # ใช้เรียก save ของ Django เพื่อบันทึกข้อมูล
        # *arg จะใช้สำหรับรับค่า Position arguments หลายๆตัว
        # **kwargs จะใช้สำหรับรับค่า Keyword arguments หลายๆตัว
        # Positon arguments ก็ค่า argument ที่ส่งไปใน function ตามตำแหน่ง
        # Keyword arguments ก็ค่า argument ที่ส่งไปใน function ตามขื่อ parameter


class Guest(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    # อันนี้ใช้ ManyToMany เพราะโจทย์ไม่ได้กำหนดว่า 1 user จองได้ห้องเดียว
    rooms = models.ManyToManyField(Room, blank=True, related_name="guests")
    hours = models.IntegerField()

    def __str__(self):
        return f"{self.first} {self.last}"
