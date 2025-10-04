from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    skidka = models.IntegerField()

    def __str__(self):
        return self.name
