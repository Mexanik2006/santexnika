from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # oddiy text saqlamaslik kerak, hash ishlatish yaxshiroq

    def __str__(self):
        return self.username
