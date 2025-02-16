from rest_framework import serializers

from .model import Todos


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = '__all__'