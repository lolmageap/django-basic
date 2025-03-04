from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Users


class PasswordValidator:
    @staticmethod
    def validate(data: dict) -> dict:
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Password does not match')
        return data


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=125)
    password_confirm = serializers.CharField(max_length=125)

    def validate(self, data: dict) -> dict:
        return PasswordValidator.validate(data)

    def create(self, validated_data: dict) -> Users:
        validated_data.pop("password_confirm")
        validated_data["password"] = make_password(validated_data["password"])
        return Users.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=125)
