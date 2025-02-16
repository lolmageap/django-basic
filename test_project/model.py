from django.db import models


class Todos(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Users(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=125)
    is_active = models.BooleanField(default=True)
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        USER = 'user'
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.USER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

