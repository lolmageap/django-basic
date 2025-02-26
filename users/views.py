from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Role
from .serializers import LoginSerializer, SignUpSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
            Role.objects.create(user=user, name=Role.Roles.USER)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response(
                data={"message": "Login successful", "access_token": access_token},
                status=status.HTTP_200_OK,
            )
            response["Authorization"] = f"Bearer {access_token}"

            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
            )

            return response
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.headers["Authorization"] = ""
        response.delete_cookie("refresh_token")
        return response
