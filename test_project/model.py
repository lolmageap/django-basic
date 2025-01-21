from django.db import models
from django.contrib.auth.models import User as AuthUser


class PayPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Organization(models.Model):
    class Industries(models.TextChoices):
        PERSONAL = 'personal'
        RETAIL = 'retail'
        MANUFACTURING = 'manufacturing'
        IT = 'it'
        OTHER = 'other'
    name = models.CharField(max_length=50)
    industry = models.CharField(max_length=20, choices=Industries.choices, default=Industries.OTHER)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Users(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)


class EmailVerification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)