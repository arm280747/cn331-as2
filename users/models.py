from django.db import models


class Name(models.Model):
    Name = models.CharField(max_length=100)
    Surname = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text
