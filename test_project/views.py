from django.contrib.auth import authenticate
from rest_framework import generics

from rest_framework import status
from tokenize import Token
from .model import Todos
from rest_framework.response import Response
from .serializers import TodoSerializer, SingUpSerializer, LoginSerializer


def perform_create(serializer: TodoSerializer) -> None:
    serializer.save()


class CreateTodoView(generics.CreateAPIView):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer


class GetTodoView(generics.RetrieveAPIView):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'


class SignUpView(generics.GenericAPIView):
    serializer_class = SingUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
