from django.db import transaction
from rest_framework import serializers

from .models import Todos


class CreateTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = 'title', 'description', 'user', 'started_at', 'ended_at'

        def validate(self, data):
            data = self.validate_initialize(data)
            data = self.validate_scheduling_time(data)
            return data

        def validate_initialize(self, data: dict) -> dict:
            title = data.get('title', '')
            if not (3 <= len(title) <= 50):
                raise serializers.ValidationError({'title': 'Title must be between 3 and 50 characters.'})
            return data

        def validate_scheduling_time(self, data: dict) -> dict:
            user = data.get('user')
            started_at = data.get('started_at').replace(second=0, microsecond=0)
            ended_at = data.get('ended_at').replace(second=0, microsecond=0)
            now = datetime.now()

            if started_at < now:
                raise serializers.ValidationError({'started_at': 'Start time must be greater than current time.'})
            if ended_at < now:
                raise serializers.ValidationError({'ended_at': 'End time must be greater than current time.'})
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


class UpdateTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ('title', 'description', 'is_completed', 'user', 'started_at', 'ended_at')

        def validate(self, data):
            data = self.validate_initialize(data)
            data = self.validate_scheduling_time(data)
            return data

        def validate_initialize(self, data: dict) -> dict:
            title = data.get('title', '')
            if not (3 <= len(title) <= 50):
                raise serializers.ValidationError({'title': 'Title must be between 3 and 50 characters.'})
            return data

        def validate_scheduling_time(self, data: dict) -> dict:
            user = data.get('user')
            started_at = data.get('started_at').replace(second=0, microsecond=0)
            ended_at = data.get('ended_at').replace(second=0, microsecond=0)
            now = datetime.now()

            if started_at < now:
                raise serializers.ValidationError({'started_at': 'Start time must be greater than current time.'})
            if ended_at < now:
                raise serializers.ValidationError({'ended_at': 'End time must be greater than current time.'})
            if started_at > ended_at:
                raise serializers.ValidationError({'ended_at': 'End time must be greater than start time.'})

            with transaction.atomic():
                todo = Todos.objects.filter(user=user, started_at__lte=started_at, ended_at__gte=ended_at)
                if todo.exists() and todo.first().id != self.instance.id:
                    raise serializers.ValidationError({'You have a task scheduled at this time.'})
            return data


class FindAllTodoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ('id', 'title', 'description', 'is_completed', 'user', 'created_at')
