from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=125)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Role(models.Model):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        EDITOR = 'editor', 'Editor'

    name = models.CharField(max_length=50, choices=Roles.choices)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='roles')

    def __str__(self):
        return self.name


class Todos(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()