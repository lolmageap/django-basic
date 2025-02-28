from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from common.exceptions import NotFoundException
from common.permissions import RoleBasedPermission
from common.pagination import CustomPagination
from .models import Todos
from .serializers import (
    CreateTodoSerializer, FindOneTodoResponseSerializer,
    FindAllTodoResponseSerializer, FindAllTodoRequestSerializer,
    UpdateTodoSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="모든 TODO 조회",
        request=FindAllTodoRequestSerializer,
        responses={status.HTTP_200_OK: FindAllTodoResponseSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="단일 TODO 조회",
        responses={status.HTTP_200_OK: FindOneTodoResponseSerializer}
    ),
    create=extend_schema(
        summary="TODO 생성",
        request=CreateTodoSerializer,
        responses={status.HTTP_201_CREATED: None}
    ),
    update=extend_schema(
        summary="TODO 수정",
        request=UpdateTodoSerializer,
        responses={status.HTTP_200_OK: None}
    ),
    destroy=extend_schema(
        summary="TODO 삭제",
        responses={status.HTTP_200_OK: None}
    )
)
class TodoViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    pagination_class = CustomPagination
    roles = ["ADMIN", "USER"]
    queryset = Todos.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTodoSerializer
        if self.action == "update":
            return UpdateTodoSerializer
        if self.action == "retrieve":
            return FindOneTodoResponseSerializer
        return FindAllTodoResponseSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset().order_by("id")
        request_serializer = FindAllTodoRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        user = request.user

        start_date = request_serializer.validated_data.get("start_date")
        end_date = request_serializer.validated_data.get("end_date")
        is_completed = request_serializer.validated_data.get("is_completed")

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if user is not None:
            queryset = queryset.filter(user=user)
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk: int, *args, **kwargs) -> Response:
        todo = self.get_queryset().filter(pk=pk, user=request.user).first()
        if not todo: raise NotFoundException("Todo not found")

        serializer = self.get_serializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save(user=request.user)
            return Response({"message": "Todo created successfully"}, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: int, *args, **kwargs) -> Response:
        todo = self.get_queryset().filter(pk=pk, user=request.user).first()
        if not todo: raise NotFoundException("Todo not found")

        serializer = self.get_serializer(todo, data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()
            return Response({"message": "Todo updated successfully"}, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk: int, *args, **kwargs) -> Response:
        todo = self.get_queryset().filter(pk=pk, user=request.user).first()
        if not todo: raise NotFoundException("Todo not found")

        todo.delete()
        return Response({"message": "Todo deleted successfully"}, status=status.HTTP_200_OK)
