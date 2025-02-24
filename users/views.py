from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, SignUpSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            response["Authorization"] = f"Bearer {access_token}"

            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax"
            )

            return response
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.headers["Authorization"] = ""
        response.delete_cookie("refresh_token")
        return response
