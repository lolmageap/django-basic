from rest_framework import generics

from .model import Todos
from .serializers import TodoSerializer


def perform_create(serializer: TodoSerializer) -> None:
    serializer.save()


class CreateTodoView(generics.CreateAPIView):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer


class GetTodoView(generics.RetrieveAPIView):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'
