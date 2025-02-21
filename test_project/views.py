from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .model import Todos
from .serializers import CreateTodoSerializer, LoginSerializer, SignUpSerializer, FindOneTodoResponseSerializer, \
    FindAllTodoResponseSerializer, FindAllTodoRequestSerializer


class CreateTodoView(generics.CreateAPIView):
    serializer_class = CreateTodoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Todo created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FindOneTodoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, pk: int):
        queryset = Todos.objects.filter(pk=pk)

        if not queryset.exists():
            return Response({"detail": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

        response_serializer = FindOneTodoResponseSerializer(queryset.first())
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class FindAllTodoView(generics.ListAPIView):
    serializer_class = FindAllTodoResponseSerializer
    queryset = Todos.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        request_serializer = FindAllTodoRequestSerializer(data=self.request.query_params)
        request_serializer.is_valid(raise_exception=True)

        start_date = request_serializer.validated_data.get('start_date')
        end_date = request_serializer.validated_data.get('end_date')
        user = request_serializer.validated_data.get('user')
        is_completed = request_serializer.validated_data.get('is_completed')

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if user is not None:
            queryset = queryset.filter(user=user)
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed)

        return queryset


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.user.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
