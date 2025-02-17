from rest_framework import generics

from .model import Todos
from .serializers import TodoSerializer, SingUpSerializer


def perform_create(serializer: TodoSerializer) -> None:
    serializer.save()


class CreateTodoView(generics.CreateAPIView):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer


class GetTodoView(generics.RetrieveAPIView):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'


class LoginView(generics.GenericAPIView):
    serializer_class = SingUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
