from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .model import Todos, Users


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = '__all__'


class PasswordValidator:
    @staticmethod
    def validate(self):
        if self['password'] != self['password_confirm']:
            raise serializers.ValidationError('Password does not match')
        return self


def create(validated_data):
    validated_data.pop("password_confirm")
    validated_data["password"] = make_password(validated_data["password"])
    return Users.objects.create(**validated_data)


class SingUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=125)
    password_confirm = serializers.CharField(max_length=125)
    __validate__ = PasswordValidator.validate
    __create__ = create

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=125)