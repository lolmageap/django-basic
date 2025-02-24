from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from .model import Todos, Users


class CreateTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = 'title', 'description', 'user', 'started_at', 'ended_at'

        def validate_initialize(self, data: dict) -> dict:
            title = data.get('title', '')
            if not (3 <= len(title) <= 50):
                raise serializers.ValidationError({'title': 'Title must be between 3 and 50 characters.'})
            return data

        def validate_scheduling_time(self, data: dict) -> dict:
            user = data.get('user')
            started_at = data.get('started_at')
            ended_at = data.get('ended_at')

            if started_at > ended_at:
                raise serializers.ValidationError({'ended_at': 'End time must be greater than start time.'})

            with transaction.atomic():
                if Todos.objects.filter(user=user, started_at__lte=started_at, ended_at__gte=ended_at).exists():
                    raise serializers.ValidationError({'You have a task scheduled at this time.'})

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
