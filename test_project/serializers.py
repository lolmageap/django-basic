from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .model import Todos, Users


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = 'title', 'description', 'is_completed', 'user'

        @staticmethod
        def validate(data):
            title = data.get('title', '')
            if not (3 <= len(title) <= 50):
                raise serializers.ValidationError({'title': 'Title must be between 3 and 50 characters.'})
            return data


class FindOneTodoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ('id', 'title', 'description', 'is_completed', 'user', 'created_at')


class FindAllTodoRequestSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    is_completed = serializers.BooleanField(required=False)


class FindAllTodoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ('id', 'title', 'description', 'is_completed', 'user', 'created_at')


class PasswordValidator:
    @staticmethod
    def validate(self):
        if self['password'] != self['password_confirm']:
            raise serializers.ValidationError('Password does not match')
        return self


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=125)
    password_confirm = serializers.CharField(max_length=125)
    __validate__ = PasswordValidator.validate

    def validate(self, data):
        return self.__validate__(data)

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        validated_data["password"] = make_password(validated_data["password"])
        return Users.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=125)
