from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, Roles
from .serializers import LoginSerializer, SignUpSerializer
from myapp.exceptions import AuthenticationFailedException


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
            Role.objects.create(user=user, name=Roles.USER)
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data["email"]
        password = request.data["password"]
        user = authenticate(self.request, email=email, password=password)

        if user is None: raise AuthenticationFailedException(f"{email} is not authenticated")
        refresh = RefreshToken.for_user(user)
        refresh["roles"] = list(Role.objects.filter(user=user).values_list("name", flat=True))
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(
            data={"message": "Login successful", "access_token": access_token},
            status=status.HTTP_200_OK,
        )
        response["Authorization"] = "Bearer " + access_token
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        return response


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self):
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.headers["Authorization"] = ""
        response.delete_cookie("refresh_token")
        return response
