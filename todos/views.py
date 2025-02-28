from django.db import transaction
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from common.exceptions import NotFoundException
from common.permissions import RoleBasedPermission
from drf_spectacular.utils import extend_schema

from .models import Todos
from .serializers import CreateTodoSerializer, FindOneTodoResponseSerializer, FindAllTodoResponseSerializer, \
    FindAllTodoRequestSerializer, UpdateTodoSerializer


class CreateTodoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    roles = ["ADMIN", "USER"]
    request = {
        'application/json': CreateTodoSerializer,
    }
    response = {
        status.HTTP_201_CREATED: None,
        status.HTTP_400_BAD_REQUEST: None,
        status.HTTP_500_INTERNAL_SERVER_ERROR: None,
    }

    @extend_schema(request=request, responses=response)
    def post(self, request, *args, **kwargs):
        serializer = CreateTodoSerializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save(user=request.user)
            return Response({"message": "Todo created successfully"}, status=status.HTTP_201_CREATED)


class FindOneTodoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    roles = ["ADMIN", "USER"]
    request = {
        'application/json': None,
    }
    response = {
        status.HTTP_200_OK: FindOneTodoResponseSerializer,
        status.HTTP_400_BAD_REQUEST: None,
        status.HTTP_404_NOT_FOUND: None,
    }

    @extend_schema(request=request, responses=response)
    def get(self, pk: int):
        queryset = Todos.objects.filter(pk=pk, user=self.request.user)

        if not queryset.exists():
            raise NotFoundException("Todo not found")

        response_serializer = FindOneTodoResponseSerializer(queryset.first())
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class FindAllTodoView(ListAPIView):
    serializer_class = FindAllTodoResponseSerializer
    queryset = Todos.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    roles = ["ADMIN", "USER"]
    request = {
        'application/json': FindAllTodoRequestSerializer,
    }
    response = {
        status.HTTP_200_OK: FindAllTodoResponseSerializer(many=True),
        status.HTTP_400_BAD_REQUEST: None,
    }

    @extend_schema(request=request, responses=response)
    def get(self, request, *args, **kwargs):
        queryset = self.queryset

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


class UpdateTodoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    roles = ["ADMIN", "USER"]
    request = {
        'application/json': UpdateTodoSerializer,
    }
    response = {
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: None,
        status.HTTP_404_NOT_FOUND: None,
    }

    @extend_schema(request=request, responses=response)
    def put(self, pk: int):
        todo = Todos.objects.filter(pk=pk, user=self.request.user).first()
        if todo is None:
            raise NotFoundException("Todo not found")

        serializer = UpdateTodoSerializer(data=self.request.data, instance=todo)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
            return Response({"message": "Todo updated successfully"}, status=status.HTTP_200_OK)


class DeleteTodoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    roles = ["ADMIN", "USER"]
    serializer_class = None
    request = {
        'application/json': None,
    }
    response = {
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: None,
        status.HTTP_404_NOT_FOUND: None,
    }

    @extend_schema(request=request, responses=response)
    def delete(self, pk: int):
        todo = Todos.objects.filter(pk=pk, user=self.request.user).first()
        if todo is None:
            raise NotFoundException("Todo not found")
        else:
            todo.delete()
            return Response({"message": "Todo deleted successfully"}, status=status.HTTP_200_OK)
